from flask import Blueprint, request, jsonify, send_file, current_app
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import re
import os
import google.generativeai as genai
from googleapiclient.discovery import build
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
from collections import Counter
import string
from dotenv import load_dotenv

analysis_bp = Blueprint('analysis_bp', __name__)

# Charger les variables d'environnement depuis le fichier .env si non déjà chargées
load_dotenv()

# --- Service Initialization ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

gemini_model = None
if GEMINI_API_KEY and GEMINI_API_KEY != "VOTRE_CLE_API_GEMINI_ICI":
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        print(f"Failed to configure Gemini: {e}")

youtube_service = None
if YOUTUBE_API_KEY and YOUTUBE_API_KEY != "VOTRE_CLE_API_YOUTUBE_ICI":
    try:
        youtube_service = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    except Exception as e:
        print(f"Failed to build YouTube service: {e}")

def extract_video_id(url):
    regex = r"(?:https?://)?(?:www\.)?(?:youtube\.com/(?:[^/\n\s]+/\S+/|(?:v|e(?:mbed)?)/|\S*?[?&]v=)|youtu\.be/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})"
    match = re.search(regex, url)
    return match.group(1) if match else None

sentiment_pipeline = None
semantic_model = None

def get_word_ranking(texts, top_n=50):
    stop_words = set(['a', 'à', 'alors', 'au', 'aucuns', 'aussi', 'autre', 'avant', 'avec', 'avoir', 'bon', 'car', 'ce', 'cela', 'ces', 'ceux', 'chaque', 'ci', 'comme', 'comment', 'dans', 'de', 'des', 'du', 'dedans', 'dehors', 'depuis', 'devrait', 'doit', 'donc', 'dos', 'début', 'elle', 'elles', 'en', 'encore', 'essai', 'est', 'et', 'eu', 'fait', 'faites', 'fois', 'font', 'hors', 'ici', 'il', 'ils', 'je', 'juste', 'la', 'le', 'les', 'leur', 'là', 'ma', 'maintenant', 'mais', 'mes', 'mien', 'moins', 'mon', 'mot', 'même', 'ni', 'nommés', 'notre', 'nous', 'nouveaux', 'ou', 'où', 'par', 'parce', 'pas', 'peut', 'peu', 'plupart', 'pour', 'pourquoi', 'quand', 'que', 'quel', 'quelle', 'quelles', 'quels', 'qui', 'sa', 'sans', 'ses', 'seulement', 'si', 'sien', 'son', 'sont', 'sous', 'soyez', 'sujet', 'sur', 'ta', 'tandis', 'tellement', 'tels', 'tes', 'ton', 'tous', 'tout', 'trop', 'très', 'tu', 'voient', 'vont', 'votre', 'vous', 'vu', 'ça', 'étaient', 'état', 'étions', 'été', 'être', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn', 'cest', 'jai', 'cest', 'sil', 'quil', 'dun', 'une', 'jai'])
    all_words = []
    translator = str.maketrans('', '', string.punctuation)
    for text in texts:
        cleaned_text = text.lower().translate(translator)
        words = cleaned_text.split()
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        all_words.extend(filtered_words)
    word_counts = Counter(all_words)
    return word_counts.most_common(top_n)

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
            font_dir = os.path.join(current_app.root_path, 'templates', 'public', 'fonts')
            arial_path = os.path.join(font_dir, 'arial.ttf')
            if os.path.exists(arial_path):
                self.add_font('Arial', '', arial_path, uni=True)
                self.font_family = 'Arial'
                arialbd_path = os.path.join(font_dir, 'G_ari_bd.TTF')
                if os.path.exists(arialbd_path): self.add_font('Arial', 'B', arialbd_path, uni=True)
                ariali_path = os.path.join(font_dir, 'G_ari_i.TTF')
                if os.path.exists(ariali_path): self.add_font('Arial', 'I', ariali_path, uni=True)
        except Exception as e:
            print(f"PDF font loading error: {e}")

    def header(self):
        self.set_font(self.font_family, 'B', 10)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, 'Mindmap de la Vidéo', 0, 0, 'L')
        logo_path = os.path.join(current_app.root_path, 'templates', 'public', 'Scriptou.png')
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
            icon_path = os.path.join(current_app.root_path, 'templates', 'public', 'youtube_icon.png')
            if os.path.exists(icon_path):
                icon_height_user_unit = 3.5 / self.k
                font_size_user_unit = font_size / self.k
                
                y_pos = self.get_y() - (font_size_user_unit / 4) - (icon_height_user_unit / 2)
                
                self.image(icon_path, x=self.get_x(), y=y_pos, h=icon_height_user_unit, link=youtube_link)

    def add_heading(self, text, level):
        font_sizes = { 2: 20, 3: 16, 4: 14, 5: 12, 6: 12 }
        colors = { 2: (0, 0, 0), 3: (50, 50, 50), 4: (100, 100, 100), 5: (140, 140, 140), 6: (170, 170, 170) }
        color = colors.get(level, (80, 80, 80))
        
        if level == 2: self.add_page()
        
        self.ln(10 if level == 2 else 5)
        self.write_with_links(text, font_sizes.get(level, 12), 'B', color)
        self.ln(5)

    def add_bullet_item(self, text, indent_level):
        bullet_colors = { 1: (30, 30, 30), 2: (80, 80, 80), 3: (130, 130, 130), }
        color = bullet_colors.get(indent_level, (160, 160, 160))

        self.ln(4)
        indent = 25 + ((indent_level -1) * 8)
        self.set_x(indent)
        self.set_font(self.font_family, '', 11)
        self.set_text_color(*color)
        self.write(0, '• ')
        self.write_with_links(text, 11, '', color)

@analysis_bp.route('/prompts', methods=['GET'])
def list_prompts_route():
    prompt_dir = os.path.join(current_app.root_path, 'prompt')
    available_prompts = []
    try:
        if os.path.exists(prompt_dir) and os.path.isdir(prompt_dir):
            for filename in os.listdir(prompt_dir):
                if filename.endswith(".txt"):
                    prompt_name = os.path.splitext(filename)[0]
                    pretty_name = " ".join(word.capitalize() for word in prompt_name.replace("_", " ").replace("-", " ").split())
                    available_prompts.append({"filename": filename, "displayName": pretty_name})
            available_prompts.sort(key=lambda x: x['displayName'])
            return jsonify(available_prompts)
        else:
            return jsonify({"error": "Dossier de prompts non trouvé."}, 500)
    except Exception as e:
        return jsonify({"error": f"Erreur serveur: {e}"}, 500)

@analysis_bp.route('/transcript', methods=['POST'])
def get_transcript_route():
    try:
        if not request.is_json:
            return jsonify({"error": "Requête invalide, JSON attendu."}, 400)
        
        data = request.get_json()
        video_url = data.get('url')
        language_preference = data.get('language', 'fr').lower()

        if not video_url:
            return jsonify({"error": "URL manquante"}), 400

        video_id = extract_video_id(video_url)
        if not video_id:
            return jsonify({"error": "URL YouTube invalide"}), 400

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
                if all_langs:
                    chosen_transcript = transcript_availability.find_generated_transcript(all_langs)
                    transcript_list_data = chosen_transcript.fetch()
                    detected_lang_code = chosen_transcript.language_code
                else:
                    raise NoTranscriptFound("Aucune langue disponible listée par list_transcripts.")

        except TranscriptsDisabled:
            return jsonify({"error": "Les transcriptions sont désactivées pour cette vidéo."}, 400)
        except NoTranscriptFound:
             return jsonify({"error": "Aucune transcription disponible pour cette vidéo."}, 404)
        except Exception as e_fetch:
            return jsonify({"error": f"Erreur lors de la récupération de la transcription: {str(e_fetch)}"}, 500)
        
        if not transcript_list_data:
             return jsonify({"error": "Aucune transcription n'a pu être chargée finalement."}, 500)

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

        video_title = "Titre non disponible"
        if youtube_service:
            try:
                video_response = youtube_service.videos().list(part='snippet', id=video_id).execute()
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
        return jsonify({"error": "Erreur interne majeure du serveur lors de la récupération du transcript."}, 500)

@analysis_bp.route('/comments', methods=['POST'])
def get_comments_route():
    if not youtube_service:
        return jsonify({"error": "Le service YouTube Data API n'est pas configuré ou la clé API est invalide."}, 503)

    try:
        if not request.is_json:
            return jsonify({"error": "Requête invalide, JSON attendu."}, 400)
        
        data = request.get_json()
        video_url = data.get('url')
        if not video_url:
            return jsonify({"error": "URL manquante"}), 400

        video_id = extract_video_id(video_url)
        if not video_id:
            return jsonify({"error": "URL YouTube invalide"}), 400

        all_comments = []
        next_page_token = None

        while True:
            request_params = {
                'part': 'snippet,replies',
                'videoId': video_id,
                'maxResults': 100
            }
            if next_page_token:
                request_params['pageToken'] = next_page_token

            response = youtube_service.commentThreads().list(**request_params).execute() 
            
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
                break

        video_title = "Titre non disponible"
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        try:
            video_response = youtube_service.videos().list(part='snippet', id=video_id).execute()
            if video_response['items']:
                snippet = video_response['items'][0]['snippet']
                video_title = snippet['title']
        except Exception:
            pass

        response_data = {
            "comments": all_comments,
            "video_title": video_title,
            "thumbnail_url": thumbnail_url
        }
        response = jsonify(response_data)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return response

    except Exception as e:
        return jsonify({"error": f"Erreur interne majeure du serveur lors de la récupération des commentaires: {e}"}, 500)

@analysis_bp.route('/gemini', methods=['POST'])
def call_gemini_route():
    if not gemini_model:
        return jsonify({"error": "Le modèle Gemini n'est pas configuré ou la clé API est invalide."}, 503)

    try:
        if not request.is_json:
            return jsonify({"error": "Requête invalide, JSON attendu."}, 400)

        data = request.get_json()
        transcript_text = data.get('transcript')
        prompt_filename = data.get('prompt_file')

        if not prompt_filename:
            return jsonify({"error": "Nom du fichier prompt manquant."}, 400)
        
        if not transcript_text or not transcript_text.strip():
            return jsonify({"error": "Le texte de la transcription est nécessaire."}, 400)

        prompt_dir = os.path.join(current_app.root_path, 'prompt')
        prompt_file_path = os.path.join(prompt_dir, prompt_filename)

        if not os.path.exists(prompt_file_path):
            return jsonify({"error": f"Fichier prompt '{prompt_filename}' non trouvé."}, 404)
        
        with open(prompt_file_path, 'r', encoding='utf-8') as f:
            prompt_template = f.read()
        
        final_prompt = prompt_template.replace("{transcript}", transcript_text)
        
        try:
            gemini_response = gemini_model.generate_content(final_prompt)
            response_text = "".join(part.text for part in gemini_response.parts if hasattr(part, 'text'))
            
            if not response_text and hasattr(gemini_response, 'prompt_feedback') and gemini_response.prompt_feedback and gemini_response.prompt_feedback.block_reason:
                return jsonify({"error": f"Requête bloquée par Gemini: {gemini_response.prompt_feedback.block_reason}"}, 400)
            
            cost_info = {}
            # Cost calculation logic can be added here if needed

        except Exception as e_gemini:
            return jsonify({"error": f"Erreur API Gemini: {str(e_gemini)}"}, 500)

        response_data = { "gemini_response": response_text, "cost_analysis": cost_info }
        response = jsonify(response_data)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return response

    except Exception as e:
        return jsonify({"error": f"Erreur interne du serveur: {e}"}, 500)

@analysis_bp.route('/analyze_comments', methods=['POST'])
def analyze_comments_route():
    if not gemini_model:
        return jsonify({"error": "Le modèle Gemini n'est pas configuré."}, 503)

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Requête invalide, JSON attendu."}, 400)

        comments = data.get('comments')
        prompt_filename = data.get('prompt_file')

        if not comments or not isinstance(comments, list):
            return jsonify({"error": "La liste des commentaires est manquante ou invalide."}, 400)
        if not prompt_filename:
            return jsonify({"error": "Le fichier de prompt est manquant."}, 400)

        comments_text = "\n\n".join([f"Auteur: {c.get('author', 'N/A')}\nCommentaire: {c.get('text', '')}" for c in comments])
        prompt_dir = os.path.join(current_app.root_path, 'prompt')
        prompt_file_path = os.path.join(prompt_dir, prompt_filename)

        if not os.path.exists(prompt_file_path):
            return jsonify({"error": f"Fichier prompt '{prompt_filename}' non trouvé."}, 404)
        
        with open(prompt_file_path, 'r', encoding='utf-8') as f:
            prompt_template = f.read()

        json_schema_prompt = "{\"type\": \"object\", \"properties\": {\"sentiment\": {\"type\": \"object\", \"properties\": {\"positive\": {\"type\": \"number\"}, \"negative\": {\"type\": \"number\"}, \"neutral\": {\"type\": \"number\"}}}, \"keyThemes\": {\"type\": \"array\", \"items\": {\"type\": \"object\", \"properties\": {\"theme\": {\"type\": \"string\"}, \"summary\": {\"type\": \"string\"}, \"exampleComment\": {\"type\": \"string\"}}}}, \"videoIdeas\": {\"type\": \"array\", \"items\": {\"type\": \"string\"}}}, \"required\": [\"sentiment\", \"keyThemes\", \"videoIdeas\"} }"
        final_prompt = f"{prompt_template}\n\nVoici la liste des commentaires à analyser:\n---\n{comments_text}\n---\n\nRéponds IMPÉRATIVEMENT avec un objet JSON valide qui correspond au schéma suivant:\n{json_schema_prompt}"
        
        generation_config = genai.types.GenerationConfig(response_mime_type="application/json")
        gemini_response = gemini_model.generate_content(final_prompt, generation_config=generation_config)
        
        response_text = gemini_response.text
        analysis_json = json.loads(response_text)
        return jsonify({"analysis_result": analysis_json})

    except json.JSONDecodeError:
        return jsonify({"error": "La réponse de l'IA n'était pas un JSON valide."}, 500)
    except Exception as e:
        return jsonify({"error": f"Erreur interne du serveur: {e}"}, 500)

@analysis_bp.route('/analyze_batch', methods=['POST'])
def analyze_batch_route():
    global sentiment_pipeline, semantic_model
    if sentiment_pipeline is None:
        sentiment_pipeline = pipeline('sentiment-analysis', model='nlptown/bert-base-multilingual-uncased-sentiment')
    if semantic_model is None:
        semantic_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    if not all([sentiment_pipeline, semantic_model, gemini_model]):
        return jsonify({"error": "Le service d'analyse n'est pas complètement initialisé."}), 503

    try:
        data = request.get_json()
        if not data or 'comments' not in data or not isinstance(data['comments'], list):
            return jsonify({"error": "Requête invalide, une liste de commentaires est attendue."}, 400)

        comments = data['comments']
        if not comments:
            return jsonify({"message": "La liste de commentaires est vide, rien à analyser."}, 200)
            
        texts_to_analyze = [c.get('text', '') for c in comments if c.get('text')]
        if not texts_to_analyze:
            return jsonify({"message": "Les commentaires fournis sont vides, rien à analyser."}, 200)

        max_length = sentiment_pipeline.tokenizer.model_max_length
        truncated_texts = [text[:max_length] for text in texts_to_analyze]
        sentiment_results = sentiment_pipeline(truncated_texts)

        embeddings = semantic_model.encode(texts_to_analyze, show_progress_bar=False)

        n_neighbors = min(15, len(texts_to_analyze) - 1)
        if n_neighbors < 2:
             return jsonify({"error": "Pas assez de commentaires pour identifier des thèmes."}, 400)

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
                "Analyse en profondeur les commentaires suivants... Réponds en JSON: {\"theme_name\": \"...\", \"theme_summary\": \"...\"}"
            )
            
            try:
                generation_config = genai.types.GenerationConfig(response_mime_type="application/json")
                gemini_response = gemini_model.generate_content(prompt, generation_config=generation_config)
                response_text = gemini_response.text
                start_index = response_text.find('{')
                end_index = response_text.rfind('}')
                if start_index != -1 and end_index != -1:
                    json_str = response_text[start_index:end_index+1]
                    theme_info = json.loads(json_str)
                    theme_name = theme_info.get("theme_name", f"Thème {theme_id}")
                    theme_summary = theme_info.get("theme_summary", "Pas de résumé.")
                else:
                    theme_name = f"Thème {theme_id}"
                    theme_summary = "Réponse non-JSON."

            except Exception as e_gemini:
                theme_name = f"Thème {theme_id}"
                theme_summary = f"Erreur Gemini: {str(e_gemini)}"

            final_themes.append({
                "themeId": int(theme_id),
                "name": theme_name,
                "summary": theme_summary,
                "commentCount": len(theme_comments),
                "comments": theme_comments
            })

        sentiments_list = []
        for i, text in enumerate(texts_to_analyze):
            sentiment_res = sentiment_results[i]
            sentiment_label = sentiment_res['label']
            if sentiment_label in ['1 star', '2 stars']: sentiment = 'négatif'
            elif sentiment_label == '3 stars': sentiment = 'neutre'
            else: sentiment = 'positif'
            sentiments_list.append({"text": text, "sentiment": sentiment, "confidence": sentiment_res['score']})

        keywords_list = [theme['name'] for theme in final_themes]
        questions_list = [text for text in texts_to_analyze if text.strip().endswith('?')] # Corrected regex
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
        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": f"Erreur interne du serveur lors de l'analyse par lot: {e}"}, 500)

@analysis_bp.route('/export_pdf', methods=['POST'])
def export_pdf_route():
    try:
        data = request.get_json()
        if not data: return jsonify({"error": "Requête invalide."}, 400)

        markdown_content = data.get('markdown')
        video_url = data.get('videoUrl')
        video_title = data.get('videoTitle')
        thumbnail_url = data.get('thumbnailUrl')

        if not markdown_content: return jsonify({"error": "Contenu Markdown manquant."}, 400)

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
        return jsonify({"error": f"Erreur interne du serveur lors de la génération du PDF: {e}"}, 500)