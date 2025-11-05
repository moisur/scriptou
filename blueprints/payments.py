from flask import Blueprint, request, jsonify
import stripe
import os
from dotenv import load_dotenv
from models import db, User
from blueprints.auth import token_required

payments_bp = Blueprint('payments_bp', __name__)

load_dotenv()
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')

stripe.api_key = STRIPE_SECRET_KEY

@payments_bp.route('/create-checkout-session', methods=['POST'])
@token_required
def create_checkout_session(current_user):
    try:
        data = request.get_json()
        price_id = data.get('priceId')

        if not price_id:
            return jsonify({'error': 'Price ID is required'}), 400

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

@payments_bp.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data()
    sig_header = request.headers.get('stripe-signature')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return str(e), 400
    except stripe.error.SignatureVerificationError as e:
        return str(e), 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_id = session.get('customer')
        
        user = User.query.filter_by(stripe_customer_id=customer_id).first()
        if user:
            user.role = 'paid'
            db.session.commit()
        
    return jsonify(success=True), 200
