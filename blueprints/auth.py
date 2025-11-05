from flask import Blueprint, request, jsonify, make_response
from functools import wraps
from models import db, User

auth_bp = Blueprint('auth_bp', __name__)

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

@auth_bp.route('/register', methods=['POST'])
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

@auth_bp.route('/login', methods=['POST'])
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
    response = make_response(jsonify({'user': {'id': user.id, 'email': user.email, 'role': user.role}}))
    response.set_cookie('token', token, httponly=True, samesite='Lax', secure=request.is_secure, max_age=3600)
    return response

@auth_bp.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    return jsonify({'user': {'id': current_user.id, 'email': current_user.email, 'role': current_user.role}})
