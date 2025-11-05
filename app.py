from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import re
import os
import google.generativeai as genai
from googleapiclient.discovery import build
import sqlite3
from datetime import datetime, timedelta
import json
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import umap
import hdbscan
import numpy as np
from fpdf import FPDF
from markdown_it import MarkdownIt
from io import BytesIO
import requests
from dotenv import load_dotenv
from collections import Counter
import string
import stripe
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import jwt
from functools import wraps
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

app = Flask(__name__, static_folder='templates/public', static_url_path='/public')
CORS(app)

# --- Configuration de la base de données ---
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASS')}"
    f"@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'super-secret-key') # Clé secrète pour JWT et sessions

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

# --- Configuration des services ---
# Clés API (chargées depuis les variables d'environnement)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
STRIPE_API_KEY = os.environ.get("STRIPE_API_KEY")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")

# Configuration de Stripe
stripe.api_key = STRIPE_API_KEY

# Configuration Google OAuth
# Les URI de redirection doivent correspondre à celles configurées dans la Google Cloud Console
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:5001/api/auth/google/callback")
SCOPES = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile', 'openid']

flow = Flow.from_client_secrets_file(
    'client_secret_569333288598-hju1hpt8u5qqoaq5fm7h1tshrf6mkh6e.apps.googleusercontent.com.json', # Chemin vers votre fichier client_secret.json
    scopes=SCOPES,
    redirect_uri=GOOGLE_REDIRECT_URI
)

# Modèle Gemini
GEMINI_MODEL_NAME = 'gemini-2.5-flash-lite'
gemini_model = None
# Service YouTube
youtube_service = None
# Modèle d'analyse de sentiment
SENTIMENT_MODEL_NAME = 'nlptown/bert-base-multilingual-uncased-sentiment'
sentiment_pipeline = None
# Modèle d'analyse sémantique
semantic_model = None

if not GEMINI_API_KEY or GEMINI_API_KEY == "VOTRE_CLE_API_GEMINI_ICI":
    pass
else:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel(GEMINI_MODEL_NAME)
    except Exception as e:
        pass

if not YOUTUBE_API_KEY or YOUTUBE_API_KEY == "VOTRE_CLE_API_YOUTUBE_ICI":
    pass
else:
    try:
        youtube_service = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    except Exception as e:
        pass

# --- Initialisation du modèle d'analyse de sentiment ---
try:
    sentiment_pipeline = pipeline('sentiment-analysis', model=SENTIMENT_MODEL_NAME)
except Exception as e:
    sentiment_pipeline = None # S'assurer que le pipeline est None en cas d'échec

# --- Initialisation du modèle d'analyse sémantique ---
try:
    SEMANTIC_MODEL_NAME = 'paraphrase-multilingual-MiniLM-L12-v2'
    semantic_model = SentenceTransformer(SEMANTIC_MODEL_NAME)
except Exception as e:
    semantic_model = None

# --- Modèle Utilisateur ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), default='user', nullable=False) # 'user', 'paid', 'admin'
    stripe_customer_id = db.Column(db.String(120), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_token(self, expires_in=3600):
        return jwt.encode(
            {'user_id': self.id, 'exp': datetime.utcnow() + timedelta(seconds=expires_in)},
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            return User.query.get(payload['user_id'])
        except jwt.ExpiredSignatureError:
            return None # Token expiré
        except jwt.InvalidTokenError:
            return None # Token invalide

    def __repr__(self):
        return f'<User {self.email}>'

# --- Décorateur pour protéger les routes ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token manquant!'}), 401
        try:
            current_user = User.verify_token(token)
            if not current_user:
                return jsonify({'message': 'Token invalide ou expiré!'}), 401
        except Exception as e:
            return jsonify({'message': 'Token invalide!', 'error': str(e)}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# --- Initialisation de la base de données ---
def init_db():
    with app.app_context():
        db.create_all()

def extract_video_id(url):
    regex = r"(?:https?://)?(?:www\.)?(?:youtube\.com/(?:[^/\n\s]+/\S+/|(?:v|e(?:mbed)?)/|\S*?[?&]v=)|youtu\.be/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})"
    match = re.search(regex, url)
    return match.group(1) if match else None

@app.route('/')
def index_page():
    return render_template('index.html')

# --- Routes d'authentification ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email et mot de passe requis'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Cet email est déjà enregistré'}), 409

    new_user = User(email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Utilisateur enregistré avec succès'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email et mot de passe requis'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Identifiants invalides'}), 401

    token = user.get_token()
    return jsonify({'token': token, 'user': {'id': user.id, 'email': user.email, 'role': user.role}})

@app.route('/api/profile', methods=['GET'])
@token_required
def profile(current_user):
    return jsonify({'user': {'id': current_user.id, 'email': current_user.email, 'role': current_user.role}})

@app.route('/api/prompts', methods=['GET'])
def list_prompts_route():
    prompt_dir = os.path.join(os.path.dirname(__file__), 'prompt')
    available_prompts = []
    try:
        if os.path.exists(prompt_dir) and os.path.isdir(prompt_dir):
            for filename in os.listdir(prompt_dir):
                if filename.endswith(".txt"):
                    # On peut prendre le nom du fichier sans l'extension pour l'affichage
                    prompt_name = os.path.splitext(filename)[0]
                    # Remplacer les underscores/tirets par des espaces et mettre en majuscule la première lettre de chaque mot pour un joli nom
                    pretty_name = " ".join(word.capitalize() for word in prompt_name.replace("_", " ").replace("-", " ").split())
                    available_prompts.append({"filename": filename, "displayName": pretty_name})
            
            # Trier les prompts par nom d'affichage pour la cohérence
            available_prompts.sort(key=lambda x: x['displayName'])
            
            return jsonify(available_prompts), 200
        else:
            return jsonify({"error": "Dossier de prompts non trouvé sur le serveur."}),
    except Exception as e:
        return jsonify({"error": "Erreur serveur lors du listage des prompts."}),

@app.route('/api/transcript', methods=['POST'])
def get_transcript_route():
    try:
        if not request.is_json:
            return jsonify({"error": "Requête invalide, JSON attendu."}),
        
        data = request.get_json()

        video_url = data.get('url')
        language_preference = data.get('language', 'fr').lower()

        if not video_url:
            return jsonify({"error": "URL manquante"}),

        video_id = extract_video_id(video_url)
        if not video_id:
            return jsonify({"error": "URL YouTube invalide"}),

        transcript_list_data = []
        detected_lang_code = None
        
        try:
            transcript_availability = YouTubeTranscriptApi.list_transcripts(video_id)
            target_langs_ordered = [language_preference]
            if language_preference != 'en': target_langs_ordered.append('en')
            if language_preference != 'fr' and 'fr' not in target_langs_ordered : target_langs_ordered.append('fr')

            for lang in target_langs_ordered:
                try:
                    chosen_transcript = transcript_availability.find_manually_created_transcript([lang])
                    transcript_list_data = chosen_transcript.fetch()
                    detected_lang_code = chosen_transcript.language_code
                    break
                except NoTranscriptFound:
                    pass
            
            if not transcript_list_data:
                for lang in target_langs_ordered:
                    try:
                        chosen_transcript = transcript_availability.find_generated_transcript([lang])
                        transcript_list_data = chosen_transcript.fetch()
                        detected_lang_code = chosen_transcript.language_code
                        break
                    except NoTranscriptFound:
                        pass
            
            if not transcript_list_data:
                all_langs = [t.language_code for t in transcript_availability]
                if all_langs: # Vérifie si la liste de langues n'est pas vide
                    chosen_transcript = transcript_availability.find_generated_transcript(all_langs)
                    transcript_list_data = chosen_transcript.fetch()
                    detected_lang_code = chosen_transcript.language_code
                else:
                    raise NoTranscriptFound("Aucune langue disponible listée par list_transcripts.")

        except TranscriptsDisabled:
            return jsonify({"error": "Les transcriptions sont désactivées pour cette vidéo."}),
        except NoTranscriptFound:
             return jsonify({"error": "Aucune transcription disponible pour cette vidéo."}),
        except Exception as e_fetch:
            return jsonify({"error": f"Erreur lors de la récupération de la transcription: {str(e_fetch)}"}),
        
        if not transcript_list_data:
             return jsonify({"error": "Aucune transcription n'a pu être chargée finalement."}),

        texts = []
        for i, item in enumerate(transcript_list_data):
            try:
                seconds = item.start
                hours = int(seconds // 3600)
                minutes = int((seconds % 3600) // 60)
                seconds_rem = int(seconds % 60)
                timestamp = f"({hours:02d}:{minutes:02d}:{seconds_rem:02d})"
                
                texts.append(f"{timestamp} {item.text}")
                
            except AttributeError:
                if hasattr(item, 'text'):
                    texts.append(item.text)
                else:
                    pass
        
        full_transcript = "\n".join(texts)
        
        if not full_transcript.strip() and transcript_list_data:
            pass

        video_title = "Titre non disponible"
        if youtube_service:
            try:
                video_response = youtube_service.videos().list(
                    part='snippet',
                    id=video_id
                ).execute()
                if video_response['items']:
                    video_title = video_response['items'][0]['snippet']['title']
            except Exception as e_title:
                pass

        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

        response_data = {
            "transcript": full_transcript,
            "thumbnail_url": thumbnail_url,
            "video_title": video_title
        }
        if detected_lang_code:
            response_data["detected_language"] = detected_lang_code
        
        response = jsonify(response_data)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return response

    except Exception as e:
        return jsonify({"error": "Erreur interne majeure du serveur lors de la récupération du transcript."}),

@app.route('/api/comments', methods=['POST'])
def get_comments_route():
    if not youtube_service:
        return jsonify({"error": "Le service YouTube Data API n'est pas configuré ou la clé API est invalide."}),

    try:
        if not request.is_json:
            return jsonify({"error": "Requête invalide, JSON attendu."}),
        
        data = request.get_json()

        video_url = data.get('url')
        if not video_url:
            return jsonify({"error": "URL manquante"}),

        video_id = extract_video_id(video_url)
        if not video_id:
            return jsonify({"error": "URL YouTube invalide"}),

        all_comments = []
        next_page_token = None

        while True:
            request_params = {
                'part': 'snippet,replies',
                'videoId': video_id,
                'maxResults': 100 # Maximum allowed per request
            }
            if next_page_token:
                request_params['pageToken'] = next_page_token

            response = youtube_service.commentThreads().list(**request_params).execute() # Correction: removed extra parenthesis
            
            for item in response.get('items', []):
                comment_data = {
                    'id': item['id'],
                    'text': item['snippet']['topLevelComment']['snippet']['textDisplay'],
                    'author': item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    'publishedAt': item['snippet']['topLevelComment']['snippet']['publishedAt'],
                    'likeCount': item['snippet']['topLevelComment']['snippet']['likeCount'],
                    'replies': []
                }
                if 'replies' in item:
                    for reply_item in item['replies']['comments']:
                        comment_data['replies'].append({
                            'id': reply_item['id'],
                            'text': reply_item['snippet']['textDisplay'],
                            'author': reply_item['snippet']['authorDisplayName'],
                            'publishedAt': reply_item['snippet']['publishedAt'],
                            'likeCount': reply_item['snippet']['likeCount']
                        })
                all_comments.append(comment_data)
            
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break # No more pages

        # Récupérer les détails de la vidéo
        video_title = "Titre non disponible"
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        try:
            video_response = youtube_service.videos().list(
                part='snippet',
                id=video_id
            ).execute()
            if video_response['items']:
                snippet = video_response['items'][0]['snippet']
                video_title = snippet['title']
                # On garde la miniature hqdefault car elle est plus grande
        except Exception:
            pass # Garder les valeurs par défaut en cas d'erreur

        response_data = {
            "comments": all_comments,
            "video_title": video_title,
            "thumbnail_url": thumbnail_url
        }
        response = jsonify(response_data)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return response

    except Exception as e:
        return jsonify({"error": f"Erreur interne majeure du serveur lors de la récupération des commentaires: {e}"}),

@app.route('/api/gemini', methods=['POST'])
def call_gemini_route():
    if not gemini_model:
        return jsonify({"error": "Le modèle Gemini n'est pas configuré ou la clé API est invalide."}),

    try:
        if not request.is_json:
            return jsonify({"error": "Requête invalide, JSON attendu."}),

        data = request.get_json()
        
        transcript_text = data.get('transcript')
        prompt_filename = data.get('prompt_file')

        if transcript_text is None:
            pass

        if not prompt_filename:
            return jsonify({"error": "Nom du fichier prompt manquant."}),
        
        if transcript_text is None or not transcript_text.strip():
            return jsonify({"error": "Le texte de la transcription est nécessaire et ne peut être vide pour l'analyse Gemini."}),

        prompt_dir = os.path.join(os.path.dirname(__file__), 'prompt')
        prompt_file_path = os.path.join(prompt_dir, prompt_filename)

        if not os.path.exists(prompt_file_path):
            return jsonify({"error": f"Fichier prompt '{prompt_filename}' non trouvé."}),
        
        with open(prompt_file_path, 'r', encoding='utf-8') as f:
            prompt_template = f.read()
        
        final_prompt = prompt_template.replace("{transcript}", transcript_text)
        
        try:
            gemini_response = gemini_model.generate_content(final_prompt)
            response_text = ""
            if hasattr(gemini_response, 'text') and gemini_response.text: # Accès direct si disponible et non vide
                response_text = gemini_response.text
            elif hasattr(gemini_response, 'parts') and gemini_response.parts: # Sinon, essayer de joindre les 'parts'
                response_text = "".join(part.text for part in gemini_response.parts if hasattr(part, 'text'))
            
            if not response_text and hasattr(gemini_response, 'prompt_feedback') and gemini_response.prompt_feedback and gemini_response.prompt_feedback.block_reason:
                block_reason_message = getattr(gemini_response.prompt_feedback, 'block_reason_message', str(gemini_response.prompt_feedback.block_reason))
                return jsonify({"error": f"La requête à Gemini a été bloquée. Raison: {block_reason_message}"}),
            elif not response_text: # Si toujours vide mais pas explicitement bloqué
                pass

            cost_info = {}
            try:
                pricing = {
                    "gemini-2.5-flash": {
                        "input": 0.35 / 1_000_000,
                        "output": 1.05 / 1_000_000
                    }
                }
                
                model_name = "gemini-2.5-flash" # Le modèle utilisé
                model_pricing = pricing.get(model_name)

                if model_pricing and hasattr(gemini_response, 'usage_metadata'):
                    usage = gemini_response.usage_metadata
                    input_tokens = usage.prompt_token_count
                    output_tokens = usage.candidates_token_count
                    
                    input_cost = input_tokens * model_pricing["input"]
                    output_cost = output_tokens * model_pricing["output"]
                    total_cost = input_cost + output_cost
                    
                    cost_info = {
                        "model_used": model_name,
                        "input_tokens": input_tokens,
                        "output_tokens": output_tokens,
                        "total_tokens": usage.total_token_count,
                        "input_cost_usd": f"{input_cost:.8f}",
                        "output_cost_usd": f"{output_cost:.8f}",
                        "total_cost_usd": f"{total_cost:.8f}"
                    }
                else:
                    cost_info = {"error": "Calcul du coût non disponible."}

            except Exception as e_cost:
                cost_info = {"error": f"Erreur lors du calcul du coût: {str(e_cost)}"}

        except Exception as e_gemini:
            error_detail = str(e_gemini)
            if hasattr(e_gemini, 'message'):
                error_detail = e_gemini.message
            return jsonify({"error": f"Erreur API Gemini: {error_detail}"}),

        response_data = {
            "gemini_response": response_text,
            "cost_analysis": cost_info
        }
        
        response = jsonify(response_data)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return response

    except Exception as e:
        return jsonify({"error": "Erreur interne majeure du serveur lors de l'appel à Gemini."}),

@app.route('/api/analyze_comments', methods=['POST'])
def analyze_comments_route():
    if not gemini_model:
        return jsonify({"error": "Le modèle Gemini n'est pas configuré."}),

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Requête invalide, JSON attendu."}),

        comments = data.get('comments')
        prompt_filename = data.get('prompt_file')

        if not comments or not isinstance(comments, list):
            return jsonify({"error": "La liste des commentaires est manquante ou invalide."}),
        if not prompt_filename:
            return jsonify({"error": "Le fichier de prompt est manquant."}),

        comments_text = "\n\n".join([f"Auteur: {c.get('author', 'N/A')}\nCommentaire: {c.get('text', '')}" for c in comments])

        prompt_dir = os.path.join(os.path.dirname(__file__), 'prompt')
        prompt_file_path = os.path.join(prompt_dir, prompt_filename)

        if not os.path.exists(prompt_file_path):
            return jsonify({"error": f"Fichier prompt '{prompt_filename}' non trouvé."}),
        
        with open(prompt_file_path, 'r', encoding='utf-8') as f:
            prompt_template = f.read()

        json_schema_prompt = """
Réponds IMPÉRATIVEMENT avec un objet JSON valide qui correspond au schéma suivant. Ne fournis AUCUN texte ou formatage en dehors de cet objet JSON.

Le schéma est:
{
    "type": "object",
    "properties": {
        "sentiment": {
            "type": "object",
            "properties": {
                "positive": {"type": "number", "description": "Pourcentage de commentaires positifs (0-100).
"},
                "negative": {"type": "number", "description": "Pourcentage de commentaires négatifs (0-100).
"},
                "neutral": {"type": "number", "description": "Pourcentage de commentaires neutres (0-100).
"}
            },
            "required": ["positive", "negative", "neutral"]
        },
        "keyThemes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "theme": {"type": "string", "description": "Titre court pour le thème clé."
},
                    "summary": {"type": "string", "description": "Résumé d'une phrase du thème."
},
                    "exampleComment": {"type": "string", "description": "Un commentaire réel qui illustre ce thème."
}
                },
                "required": ["theme", "summary", "exampleComment"]
            }
        },
        "videoIdeas": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Liste de 3 nouvelles idées de vidéos basées sur les commentaires."
        }
    },
    "required": ["sentiment", "keyThemes", "videoIdeas"]
}
"""
        
        final_prompt = f"{prompt_template}\n\nVoici la liste des commentaires à analyser:\n---\n{comments_text}\n---\n\n{json_schema_prompt}"
        
        generation_config = genai.types.GenerationConfig(
            response_mime_type="application/json"
        )
        gemini_response = gemini_model.generate_content(
            final_prompt,
            generation_config=generation_config
        )
        
        response_text = gemini_response.text

        import json
        try:
            analysis_json = json.loads(response_text)
            return jsonify({"analysis_result": analysis_json}),
        except json.JSONDecodeError:
            return jsonify({"error": "La réponse de l'IA n'était pas un JSON valide."}),

    except Exception as e:
        return jsonify({"error": "Erreur interne du serveur lors de l'analyse des commentaires."}),

def save_analysis_to_db(themes_data):
    """Sauvegarde les résultats de l'analyse (sentiments, thèmes) dans la base de données."""
    # Cette fonction est maintenant obsolète pour la table 'comments' et devrait être revue si nécessaire.
    # Les commentaires seront liés aux utilisateurs via une autre logique.
    pass

@app.route('/api/analyze_batch', methods=['POST'])
def analyze_batch_route():
    if not sentiment_pipeline or not semantic_model or not gemini_model:
        return jsonify({"error": "Le service d'analyse n'est pas complètement initialisé."}),

    try:
        data = request.get_json()
        if not data or 'comments' not in data or not isinstance(data['comments'], list):
            return jsonify({"error": "Requête invalide, une liste de commentaires est attendue."}),

        comments = data['comments']
        if not comments:
            return jsonify({"message": "La liste de commentaires est vide, rien à analyser."}),
            
        texts_to_analyze = [c.get('text', '') for c in comments if c.get('text')]
        if not texts_to_analyze:
            return jsonify({"message": "Les commentaires fournis sont vides, rien à analyser."}),

        max_length = sentiment_pipeline.tokenizer.model_max_length
        truncated_texts = [text[:max_length] for text in texts_to_analyze]
        sentiment_results = sentiment_pipeline(truncated_texts)

        embeddings = semantic_model.encode(texts_to_analyze, show_progress_bar=False)

        n_neighbors = min(15, len(texts_to_analyze) - 1)
        if n_neighbors < 2:
             return jsonify({"error": "Pas assez de commentaires pour identifier des thèmes."}),

        umap_embeddings = umap.UMAP(n_neighbors=n_neighbors, n_components=20, min_dist=0.0, metric='cosine').fit_transform(embeddings)
        min_cluster_size = max(5, int(len(texts_to_analyze) * 0.04))

        clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, metric='euclidean', cluster_selection_method='eom').fit(umap_embeddings)
        labels = clusterer.labels_

        grouped_comments = {}
        for i, label in enumerate(labels):
            if label not in grouped_comments:
                grouped_comments[label] = []
            
            sentiment_res = sentiment_results[i]
            sentiment_label = sentiment_res['label']
            if sentiment_label in ['1 star', '2 stars']: sentiment = 'négatif'
            elif sentiment_label == '3 stars': sentiment = 'neutre'
            else: sentiment = 'positif'

            comment_data = comments[i]
            comment_data['sentiment'] = sentiment
            comment_data['confidence'] = sentiment_res['score']
            grouped_comments[label].append(comment_data)

        final_themes = []
        for theme_id, theme_comments in grouped_comments.items():
            if theme_id == -1:
                continue

            sample_comments_text = "\n".join([f"- {c['text']}" for c in theme_comments[:10]])
            prompt = (
                "Analyse en profondeur les commentaires suivants, qui appartiennent tous au même groupe sémantique. "
                "Identifie le sujet PRÉCIS et SPÉCIFIQUE qui les unit. Ton objectif est de trouver le concept le plus saillant et distinctif."
                "Réponds IMPÉRATIVEMENT au format JSON suivant, sans aucun texte supplémentaire:"
                "{\"theme_name\": \"Titre de 2-4 mots capturant l'idée centrale\", \"theme_summary\": \"Un résumé d'une phrase qui explique le thème.\"}"

                "Évite les titres génériques comme 'Avis sur le produit' ou 'Questions des utilisateurs'. Sois spécifique."

                f"Commentaires à analyser:\n{sample_comments_text}"
            )
            
            try:
                generation_config = genai.types.GenerationConfig(response_mime_type="application/json")
                gemini_response = gemini_model.generate_content(prompt, generation_config=generation_config)
                
                # Nettoyage de la réponse pour extraire uniquement le JSON
                response_text = gemini_response.text
                # Trouve le premier '{' et le dernier '}' pour extraire l'objet JSON
                start_index = response_text.find('{')
                end_index = response_text.rfind('}')
                
                if start_index != -1 and end_index != -1 and end_index > start_index:
                    json_str = response_text[start_index:end_index+1]
                    theme_info = json.loads(json_str)
                    theme_name = theme_info.get("theme_name")
                    theme_summary = theme_info.get("theme_summary")
                    
                    # Si le nom du thème est vide ou non trouvé, on utilise un nom par défaut
                    if not theme_name:
                        theme_name = f"Thème {theme_id}"
                    if not theme_summary:
                        theme_summary = "Pas de résumé disponible."
                else:
                    # Si aucun JSON n'est trouvé, valeurs par défaut
                    theme_name = f"Thème {theme_id}"
                    theme_summary = "Réponse de l'IA non conforme (JSON non trouvé)."

            except Exception as e_gemini:
                theme_name = f"Thème {theme_id}"
                theme_summary = f"Erreur lors de la génération du résumé: {str(e_gemini)}"

            final_themes.append({
                "themeId": int(theme_id),
                "name": theme_name,
                "summary": theme_summary,
                "commentCount": len(theme_comments),
                "comments": theme_comments
            })

        # save_analysis_to_db(final_themes) # Désactivé pour le moment

        sentiments_list = []
        for i, text in enumerate(texts_to_analyze):
            sentiment_res = sentiment_results[i]
            sentiment_label = sentiment_res['label']
            if sentiment_label in ['1 star', '2 stars']: sentiment = 'négatif'
            elif sentiment_label == '3 stars': sentiment = 'neutre'
            else: sentiment = 'positif'
            sentiments_list.append({
                "text": text,
                "sentiment": sentiment,
                "confidence": sentiment_res['score']
            })

        keywords_list = [theme['name'] for theme in final_themes]
        questions_list = [text for text in texts_to_analyze if text.strip().endswith('?')]

        word_ranking = get_word_ranking(texts_to_analyze)

        response_data = {
            "analysis": {
                "sentiments": sentiments_list,
                "keywords": keywords_list,
                "questions": questions_list,
                "themes": final_themes,
                "word_ranking": word_ranking
            }
        }
        
        return jsonify(response_data),

    except Exception as e:
        return jsonify({"error": f"Erreur interne du serveur lors de l'analyse par lot: {e}"}),

def get_word_ranking(texts, top_n=50):
    """Compte la fréquence des mots dans une liste de textes et retourne les plus courants."""
    
    # Mots vides courants en français et anglais à exclure
    stop_words = set([
        'a', 'à', 'alors', 'au', 'aucuns', 'aussi', 'autre', 'avant', 'avec', 'avoir',
        'bon', 'car', 'ce', 'cela', 'ces', 'ceux', 'chaque', 'ci', 'comme', 'comment',
        'dans', 'de', 'des', 'du', 'dedans', 'dehors', 'depuis', 'devrait', 'doit',
        'donc', 'dos', 'début', 'elle', 'elles', 'en', 'encore', 'essai', 'est', 'et',
        'eu', 'fait', 'faites', 'fois', 'font', 'hors', 'ici', 'il', 'ils', 'je',
        'juste', 'la', 'le', 'les', 'leur', 'là', 'ma', 'maintenant', 'mais', 'mes',
        'mien', 'moins', 'mon', 'mot', 'même', 'ni', 'nommés', 'notre', 'nous',
        'nouveaux', 'ou', 'où', 'par', 'parce', 'pas', 'peut', 'peu', 'plupart',
        'pour', 'pourquoi', 'quand', 'que', 'quel', 'quelle', 'quelles', 'quels',
        'qui', 'sa', 'sans', 'ses', 'seulement', 'si', 'sien', 'son', 'sont', 'sous',
        'soyez', 'sujet', 'sur', 'ta', 'tandis', 'tellement', 'tels', 'tes', 'ton',
        'tous', 'tout', 'trop', 'très', 'tu', 'voient', 'vont', 'votre', 'vous',
        'vu', 'ça', 'étaient', 'état', 'étions', 'été', 'être',
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
        'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
        'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
        'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
        'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
        'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
        'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
        'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
        'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
        'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each',
        'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
        'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just',
        'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren',
        'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn',
        'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn',
        'cest', 'jai', 'cest', 'sil', 'quil', 'dun', 'une', 'jai'
    ])

    all_words = []
    # Créer une table de traduction pour supprimer la ponctuation
    translator = str.maketrans('', '', string.punctuation)

    for text in texts:
        # Mettre en minuscule et supprimer la ponctuation
        cleaned_text = text.lower().translate(translator)
        words = cleaned_text.split()
        # Filtrer les mots vides et les mots trop courts
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        all_words.extend(filtered_words)

    word_counts = Counter(all_words)
    return word_counts.most_common(top_n)

@app.route('/api/export_data', methods=['GET'])
def export_data_route():
    """Endpoint temporaire pour exporter les données de la table des commentaires en JSON."""
    # Cette fonction est maintenant obsolète pour la table 'comments' et devrait être revue si nécessaire.
    # Les commentaires seront liés aux utilisateurs via une autre logique.
    pass

@app.route('/api/create-checkout-session', methods=['POST'])
@token_required
def create_checkout_session(current_user):
    try:
        data = request.get_json()
        price_id = data.get('priceId')

        if not price_id:
            return jsonify({'error': 'Price ID is required'}), 400

        # Créer un client Stripe si l'utilisateur n'en a pas déjà un
        if not current_user.stripe_customer_id:
            customer = stripe.Customer.create(email=current_user.email)
            current_user.stripe_customer_id = customer.id
            db.session.commit()
        
        checkout_session = stripe.checkout.Session.create(
            customer=current_user.stripe_customer_id,
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=request.host_url + 'success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.host_url + 'cancel',
        )
        return jsonify({'sessionId': checkout_session.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stripe-webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data()
    sig_header = request.headers.get('stripe-signature')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return str(e), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return str(e), 400

    # Gérer l'événement
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_id = session.get('customer')
        
        user = User.query.filter_by(stripe_customer_id=customer_id).first()
        if user:
            user.role = 'paid'
            db.session.commit()
            # Vous pouvez également gérer l'abonnement ici si nécessaire
            # subscription_id = session.get('subscription')
            # user.stripe_subscription_id = subscription_id
            # db.session.commit()
        
    return jsonify(success=True), 200

class PDF(FPDF):
    def __init__(self, video_url=None, video_title=None, thumbnail_url=None):
        super().__init__()
        self.video_url = video_url
        self.video_title = video_title
        self.thumbnail_url = thumbnail_url
        self.video_id = extract_video_id(video_url) if video_url else None
        self.set_margins(20, 20, 20)
        self.set_auto_page_break(auto=True, margin=20)
        self.font_family = 'helvetica'
        try:
            font_dir = os.path.join(app.static_folder, 'fonts')
            arial_path = os.path.join(font_dir, 'arial.ttf')
            if os.path.exists(arial_path):
                self.add_font('Arial', '', arial_path, uni=True)
                self.font_family = 'Arial'
                arialbd_path = os.path.join(font_dir, 'G_ari_bd.TTF')
                if os.path.exists(arialbd_path): self.add_font('Arial', 'B', arialbd_path, uni=True)
                ariali_path = os.path.join(font_dir, 'G_ari_i.TTF')
                if os.path.exists(ariali_path): self.add_font('Arial', 'I', ariali_path, uni=True)
        except Exception as e:
            pass

    def header(self):
        self.set_font(self.font_family, 'B', 10)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, 'Mindmap de la Vidéo', 0, 0, 'L')
        logo_path = os.path.join(app.static_folder, 'Scriptou.png')
        if os.path.exists(logo_path): self.image(logo_path, x=self.w - 30, y=15, w=10)
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font(self.font_family, 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_title_page(self, main_title):
        self.add_page()
        if self.thumbnail_url:
            try:
                response = requests.get(self.thumbnail_url, stream=True)
                if response.status_code == 200:
                    img_buffer = BytesIO(response.content)
                    self.image(img_buffer, x='C', y=30, w=self.w / 1.5)
            except Exception as e:
                pass
        
        self.set_y(self.get_y() + 100)
        if self.video_title:
            self.set_font(self.font_family, 'B', 24)
            self.set_text_color(0, 0, 0)
            self.multi_cell(0, 12, self.video_title, 0, 'C')
            self.ln(10)

        self.set_font(self.font_family, 'I', 16)
        self.set_text_color(80, 80, 80)
        self.multi_cell(0, 10, main_title, 0, 'C')

    def write_with_links(self, text, font_size, style='', color=(50,50,50)):
        self.set_font(self.font_family, style, font_size)
        self.set_text_color(*color)
        
        clean_text = re.sub(r'\s*\(\d{1,2}:\d{2}(?:\d{2})?\)\s*$', '', text)
        self.write(0, clean_text)

        match_time = re.search(r'\((\d{1,2}:\d{2}(?:\d{2})?)\)', text)
        if self.video_id and match_time:
            timestamp = match_time.group(1)
            time_parts = list(map(int, timestamp.split(':')))
            seconds = sum(p * 60**i for i, p in enumerate(reversed(time_parts)))
            youtube_link = f"https://www.youtube.com/watch?v={self.video_id}&t={seconds}s"
            
            self.set_x(self.get_x() + 2)
            icon_path = os.path.join(app.static_folder, 'youtube_icon.png')
            if os.path.exists(icon_path):
                icon_height_user_unit = 3.5 / self.k
                font_size_user_unit = font_size / self.k
                
                y_pos = self.get_y() - (font_size_user_unit / 4) - (icon_height_user_unit / 2)
                
                self.image(icon_path, x=self.get_x(), y=y_pos, h=icon_height_user_unit, link=youtube_link)

    def add_heading(self, text, level):
        font_sizes = {2: 20, 3: 16, 4: 14, 5: 12, 6: 12}
        colors = {
            2: (0, 0, 0),
            3: (50, 50, 50),
            4: (100, 100, 100),
            5: (140, 140, 140),
            6: (170, 170, 170)
        }
        color = colors.get(level, (80, 80, 80))
        
        if level == 2: self.add_page()
        
        self.ln(10 if level == 2 else 5)
        self.write_with_links(text, font_sizes.get(level, 12), 'B', color)
        self.ln(5)

    def add_bullet_item(self, text, indent_level):
        bullet_colors = {
            1: (30, 30, 30),
            2: (80, 80, 80),
            3: (130, 130, 130),
        }
        color = bullet_colors.get(indent_level, (160, 160, 160))

        self.ln(4)
        indent = 25 + ((indent_level -1) * 8)
        self.set_x(indent)
        self.set_font(self.font_family, '', 11)
        self.set_text_color(*color)
        self.write(0, '• ')
        self.write_with_links(text, 11, '', color)

@app.route('/api/export_pdf', methods=['POST'])
def export_pdf_route():
    try:
        data = request.get_json()
        if not data: return jsonify({"error": "Requête invalide."}),

        markdown_content = data.get('markdown')
        video_url = data.get('videoUrl')
        video_title = data.get('videoTitle')
        thumbnail_url = data.get('thumbnailUrl')

        if not markdown_content: return jsonify({"error": "Contenu Markdown manquant."}),

        md = MarkdownIt()
        tokens = md.parse(markdown_content)
        
        pdf = PDF(video_url=video_url, video_title=video_title, thumbnail_url=thumbnail_url)
        
        main_title = ""
        if tokens and tokens[0].type == 'heading_open' and tokens[0].tag == 'h1':
            main_title = tokens[1].content.strip()
        
        pdf.add_title_page(main_title)

        i, list_level = 3, 0
        while i < len(tokens):
            token = tokens[i]
            if token.type == 'heading_open':
                pdf.add_heading(tokens[i+1].content.strip(), int(token.tag[1]))
                i += 2
            elif token.type == 'bullet_list_open':
                list_level += 1
                i += 1
            elif token.type == 'bullet_list_close':
                list_level = max(0, list_level - 1)
                i += 1
            elif token.type == 'list_item_open':
                pdf.add_bullet_item(tokens[i+2].content.strip(), list_level)
                i += 3
            else:
                i += 1
        
        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)

        return send_file(pdf_buffer, as_attachment=True, download_name='mindmap_final.pdf', mimetype='application/pdf')

    except Exception as e:
        return jsonify({"error": "Erreur interne du serveur lors de la génération du PDF."}),

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001, debug=False)
