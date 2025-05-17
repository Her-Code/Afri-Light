import os
import requests
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource,Api
from functools import wraps
from flask_mail import Mail,Message
from utils.email import send_email

from models.db import db
from models.user import User
from models.transaction import Transaction
from models.wallet import Wallet
from models.remittance import Remittance
from decimal import Decimal, InvalidOperation
from models.exchange_rate import ExchangeRate
from models.lightninginvoice import LightningInvoice
from models.escrow import Escrow
from models.payment_method import PaymentMethod
from models.mobile_money_prov import MobileMoneyProv

from lnd.lnd_client import lnd
from lnd import InvoiceStreamer
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///afrilight.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

 # Email configuration from environment variables
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

# mail.init_app(app)

db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
api = Api(app)
mail = Mail(app)



# Start InvoiceStreamer when app runs
invoice_streamer = InvoiceStreamer(lnd)
with app.app_context():
    invoice_streamer.start()

# --- Helper decorators ---

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user = User.query.get(get_jwt_identity())
        if not user or not getattr(user, 'is_admin', False):
            return jsonify({'message': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper


class UsersResource(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        return jsonify({'message': 'Users fetched successfully', 'status': 200, 'data': users})

    def post(self):
        data = request.get_json()

        if 'username' not in data or 'email' not in data:
            return jsonify({'message': 'Missing required fields', 'status': 400})

        existing_user = User.query.filter_by(email=data['email']).first()

        if existing_user:
            return jsonify({'message': 'User with this email already exists', 'status': 400})

        new_user = User(username=data['username'], email=data['email'])
        new_user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.id)

        return jsonify({
            'message': 'User created successfully',
            'status': 201,
            'data': new_user.to_dict(),
            'access_token': access_token
        })
app.add_resource(UsersResource, '/users')

class UserByID(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()

        if user is None:
            return jsonify({'message': 'User not found', 'status': 404})

        return jsonify({'message': 'User fetched successfully', 'status': 200, 'data': user.to_dict()})

    def patch(self, id):
        user = User.query.filter_by(id=id).first()

        if user is None:
            return jsonify({'message': 'User not found', 'status': 404})

        data = request.get_json()

        if 'profile_picture' in data:
            user.profile_picture = data['profile_picture']

        for attr, value in data.items():
            if attr != 'profile_picture':  # Skip profile_picture as it's handled separately
                setattr(user, attr, value)

        db.session.commit()

        return jsonify({'message': 'User updated successfully', 'status': 200, 'data': user.to_dict()})

    def delete(self, id):
        user = User.query.filter_by(id=id).first()

        if user is None:
            return jsonify({'message': 'User not found', 'status': 404})

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User successfully deleted', 'status': 200})
app.add_resource(UserByID, '/users/<int:id>')

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()

        if not data or 'username' not in data or 'email' not in data or 'password' not in data:
            return jsonify({'message': 'Missing required fields', 'status': 400})

        existing_user = User.query.filter_by(email=data['email']).first()

        if existing_user:
            return jsonify({'message': 'User with this email already exists', 'status': 400})

        new_user = User(username=data['username'], email=data['email'])
        new_user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.id)

        return jsonify({
            'message': 'User registered successfully',
            'status': 201,
            'data': new_user.to_dict(),
            'access_token': access_token
        })
app.add_resource(UserRegistration, '/register')
    
class Login(Resource):
    def post(self):
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)

            return jsonify({
                'message': 'Login successful',
                'status': 200,
                'access_token': access_token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'profile_picture': user.profile_picture  # Include profile picture
                }
            })

        return jsonify({'message': 'Invalid credentials', 'status': 401})
api.add_resource(Login, '/login')


# --- Wallet Resources ---

# class WalletBalanceResource(Resource):
#     @jwt_required()
#     def get(self):
#         user_id = get_jwt_identity()
#         wallet = Wallet.query.filter_by(user_id=user_id).first()
#         if not wallet:
#             return {'message': 'Wallet not found'}, 404
#         return {
#             'balance_btc': wallet.balance_btc,
#             'balance_fiat': wallet.balance_fiat
#         }

class WalletBalanceResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        wallet = Wallet.query.filter_by(user_id=user_id).first()
        if not wallet:
            return {'message': 'Wallet not found'}, 404

        return {
            'balance_fiat': float(wallet.balance_fiat),   # decimal → float for JSON
            'balance_sats': wallet.balance_sats     # integer sats, no conversion needed
        }

class WalletFundResource(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()

        amount_fiat = data.get('amount_fiat')
        amount_sats = data.get('amount_sats')

        wallet = Wallet.query.filter_by(user_id=user_id).first()
        if not wallet:
            return {'message': 'Wallet not found'}, 404

        if amount_fiat:
            if amount_fiat <= 0:
                return {'message': 'Invalid fiat amount'}, 400
            wallet.balance_fiat += amount_fiat

        if amount_sats:
            if amount_sats <= 0:
                return {'message': 'Invalid sats amount'}, 400
            wallet.balance_sats += amount_sats

        db.session.commit()

        return {
            'message': 'Wallet funded successfully',
            'new_balance_fiat': float(wallet.balance_fiat),
            'new_balance_sats': wallet.balance_sats
        }

class WalletWithdrawResource(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()

        amount_fiat = data.get('amount_fiat')
        amount_sats = data.get('amount_sats')

        wallet = Wallet.query.filter_by(user_id=user_id).first()
        if not wallet:
            return {'message': 'Wallet not found'}, 404

        if amount_fiat:
            if amount_fiat <= 0:
                return {'message': 'Invalid fiat amount'}, 400
            if wallet.balance_fiat < amount_fiat:
                return {'message': 'Insufficient fiat balance'}, 400
            wallet.balance_fiat -= amount_fiat

        if amount_sats:
            if amount_sats <= 0:
                return {'message': 'Invalid sats amount'}, 400
            if wallet.balance_sats < amount_sats:
                return {'message': 'Insufficient sats balance'}, 400
            wallet.balance_sats -= amount_sats

        db.session.commit()

        return {
            'message': 'Withdrawal successful',
            'new_balance_fiat': float(wallet.balance_fiat),
            'new_balance_sats': wallet.balance_sats
        }

api.add_resource(WalletBalanceResource, '/wallet/balance')
api.add_resource(WalletFundResource, '/wallet/fund')
api.add_resource(WalletWithdrawResource, '/wallet/withdraw')


# --- Remittance Resources ---

class RemittanceCreateResource(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json() or {}

        receiver_id = data.get('receiver_id')
        amount = data.get('amount')
        currency = (data.get('currency') or '').strip().upper()
        preferred_payout_currency = data.get('preferred_payout_currency')

        # Validate required fields
        if not receiver_id or not amount or not currency:
            return {'message': 'Missing required fields: receiver_id, amount, and currency'}, 400

        # Validate amount using Decimal
        try:
            amount_decimal = Decimal(str(amount))
            if amount_decimal <= 0:
                return {'message': 'Amount must be greater than zero'}, 400
        except (InvalidOperation, TypeError):
            return {'message': 'Invalid amount format'}, 400

        # Lookup receiver user
        receiver = User.query.get(receiver_id)
        if not receiver:
            return {'message': 'Receiver not found'}, 404

        # Determine payout currency (override if provided)
        if preferred_payout_currency:
            payout_currency = preferred_payout_currency.strip().upper()
        else:
            payout_currency = (receiver.preferred_payout_currency or 'BTC').upper()

        # Convert sender’s amount to sats (smallest BTC unit) and fiat equivalent
        amount_sats = None
        amount_fiat = None
        exchange_rate_used = None

        if currency != 'BTC':
            rate_to_btc = ExchangeRate.query.filter_by(from_currency=currency, to_currency='BTC').first()
            if not rate_to_btc:
                return {'message': f'No exchange rate from {currency} to BTC found'}, 400
            try:
                rate_decimal = Decimal(str(rate_to_btc.rate))
                amount_sats = int((amount_decimal * rate_decimal * Decimal('1e8')).to_integral_value())
            except (InvalidOperation, TypeError):
                return {'message': 'Error calculating sats amount'}, 500
            amount_fiat = float(amount_decimal)  # original fiat amount sent by sender
            exchange_rate_used = float(rate_decimal)
        else:
            # BTC to sats conversion
            amount_sats = int((amount_decimal * Decimal('1e8')).to_integral_value())

            if payout_currency != 'BTC':
                rate_btc_to_fiat = ExchangeRate.query.filter_by(from_currency='BTC', to_currency=payout_currency).first()
                if not rate_btc_to_fiat:
                    return {'message': f'No exchange rate from BTC to {payout_currency} found'}, 400
                try:
                    rate_decimal = Decimal(str(rate_btc_to_fiat.rate))
                    amount_fiat = float((amount_decimal * rate_decimal).quantize(Decimal('.01')))
                    exchange_rate_used = float(rate_decimal)
                except (InvalidOperation, TypeError):
                    return {'message': 'Error calculating fiat amount'}, 500
            else:
                amount_fiat = 0.0
                exchange_rate_used = None

        remittance = Remittance(
            sender_id=user_id,
            receiver_id=receiver_id,
            receiver_name=receiver.name,
            receiver_phone=receiver.phone,
            amount_sats=amount_sats,
            amount_fiat=amount_fiat,
            status='pending',
            payment_method_id=data.get('payment_method_id'),  # optional
            receiver_currency=payout_currency,
            preferred_payout_currency=payout_currency,
            exchange_rate_used=exchange_rate_used
        )

        db.session.add(remittance)
        db.session.commit()

        return {
            'message': 'Remittance created',
            'remittance_id': remittance.id,
            'amount_sats': amount_sats,
            'amount_fiat': amount_fiat,
            'preferred_payout_currency': payout_currency,
            'exchange_rate_used': exchange_rate_used
        }, 201

# class RemittanceCreateResource(Resource):
#     @jwt_required()
#     def post(self):
#         user_id = get_jwt_identity()
#         data = request.get_json()

#         receiver_id = data.get('receiver_id')
#         amount = data.get('amount')
#         currency = data.get('currency', '').upper()
#         preferred_payout_currency = data.get('preferred_payout_currency', None)  # optional override from sender

#         if not receiver_id or not amount or not currency:
#             return {'message': 'Missing fields'}, 400

#         receiver = User.query.get(receiver_id)
#         if not receiver:
#             return {'message': 'Receiver not found'}, 404

#         # Determine the receiver's payout currency preference (override if provided)
#         payout_currency = (preferred_payout_currency.upper() if preferred_payout_currency else receiver.preferred_payout_currency).upper()

#         # Convert the sender’s amount to sats (BTC smallest unit)
#         if currency != 'BTC':
#             rate_to_btc = ExchangeRate.query.filter_by(from_currency=currency, to_currency='BTC').first()
#             if not rate_to_btc:
#                 return {'message': f'No exchange rate from {currency} to BTC found'}, 400
#             amount_sats = int(float(amount) * rate_to_btc.rate * 1e8)  # Convert BTC to sats
#             amount_fiat = float(amount)  # original fiat amount sent by sender
#             exchange_rate_used = rate_to_btc.rate
#         else:
#             amount_sats = int(float(amount) * 1e8)  # convert BTC to sats
#             # For fiat equivalent, convert from BTC to receiver's fiat currency if needed
#             if payout_currency != 'BTC':
#                 rate_btc_to_fiat = ExchangeRate.query.filter_by(from_currency='BTC', to_currency=payout_currency).first()
#                 if not rate_btc_to_fiat:
#                     return {'message': f'No exchange rate from BTC to {payout_currency} found'}, 400
#                 amount_fiat = float(amount) * rate_btc_to_fiat.rate
#                 exchange_rate_used = rate_btc_to_fiat.rate
#             else:
#                 amount_fiat = 0  # no fiat involved
#                 exchange_rate_used = None

#         remittance = Remittance(
#             sender_id=user_id,
#             receiver_id=receiver_id,
#             receiver_name=receiver.name,
#             receiver_phone=receiver.phone,
#             amount_sats=amount_sats,
#             amount_fiat=amount_fiat,
#             status='pending',
#             payment_method_id=data.get('payment_method_id'),  # assuming sender provides
#             receiver_currency=payout_currency,
#             preferred_payout_currency=payout_currency,
#             exchange_rate_used=exchange_rate_used
#         )

#         db.session.add(remittance)
#         db.session.commit()

#         return {
#             'message': 'Remittance created',
#             'remittance_id': remittance.id,
#             'amount_sats': amount_sats,
#             'amount_fiat': amount_fiat,
#             'preferred_payout_currency': payout_currency,
#             'exchange_rate_used': exchange_rate_used
#         }, 201

class RemittanceStatusResource(Resource):
    @jwt_required()
    def get(self, remittance_id):
        user_id = get_jwt_identity()
        remittance = Remittance.query.get(remittance_id)
        if not remittance:
            return {'message': 'Remittance not found'}, 404

        # Only sender or receiver can check status
        if user_id not in [remittance.sender_id, remittance.receiver_id]:
            return {'message': 'Unauthorized'}, 403

        return {
            'remittance_id': remittance.id,
            'status': remittance.status
        }

    @jwt_required()
    def patch(self, remittance_id):
        user_id = get_jwt_identity()
        remittance = Remittance.query.get(remittance_id)
        if not remittance:
            return {'message': 'Remittance not found'}, 404

        if user_id != remittance.receiver_id:
            return {'message': 'Only receiver can update status'}, 403

        data = request.get_json()
        new_status = data.get('status')
        allowed_statuses = ['pending', 'completed', 'canceled', 'failed']

        if new_status not in allowed_statuses:
            return {'message': f'Invalid status. Allowed: {allowed_statuses}'}, 400

        remittance.status = new_status
        db.session.commit()

        return {'message': 'Status updated', 'new_status': remittance.status}
    
class RemittancePreferenceResource(Resource):

    @jwt_required()
    def get(self, remittance_id):
        user_id = get_jwt_identity()
        remittance = Remittance.query.get_or_404(remittance_id)

        if user_id not in [remittance.sender_id, remittance.receiver_id]:
            return {'message': 'Unauthorized'}, 403

        return {
            'remittance_id': remittance.id,
            'preferred_payout_currency': remittance.preferred_payout_currency
        }, 200

    @jwt_required()
    def put(self, remittance_id):
        user_id = get_jwt_identity()
        remittance = Remittance.query.get_or_404(remittance_id)

        # Ensure the user is the receiver of the remittance
        if remittance.receiver_id != user_id:
            return {'message': 'Unauthorized'}, 403

        data = request.get_json()
        preferred_currency = data.get('preferred_payout_currency', '').upper()

        if preferred_currency not in ['BTC', 'USD', 'EUR', ...]:  # list allowed currencies
            return {'message': 'Invalid payout currency'}, 400

        remittance.preferred_payout_currency = preferred_currency
        db.session.commit()

        return {
            'message': 'Preferred payout currency updated',
            'remittance_id': remittance.id,
            'preferred_payout_currency': remittance.preferred_payout_currency
        }, 200

    
api.add_resource(RemittanceCreateResource, '/remittance')
api.add_resource(RemittanceStatusResource, '/remittance/<int:remittance_id>')
api.add_resource(RemittancePreferenceResource, '/remittances/<int:remittance_id>/payout-preference')


# --- LightningInvoice Resources ---

class LightningInvoiceCreateResource(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        amount = data.get('amount')
        memo = data.get('memo', '')

        if not amount or int(amount) <= 0:
            return {'message': 'Invalid amount'}, 400

        # Call real LND gRPC to create invoice
        invoice_data = lnd.add_invoice(value=int(amount), memo=memo)

        invoice = LightningInvoice(
            user_id=user_id,
            amount=int(amount),
            memo=memo,
            status='pending',
            payment_request=invoice_data.payment_request,
            r_hash_hex=invoice_data.r_hash.hex()
        )
        db.session.add(invoice)
        db.session.commit()

        return {
            'invoice_id': invoice.id,
            'payment_request': invoice.payment_request
        }, 201
    # @jwt_required()
    # def post(self):
    #     user_id = get_jwt_identity()
    #     data = request.get_json()
    #     amount = data.get('amount')
    #     memo = data.get('memo', '')
    #     if not amount or amount <= 0:
    #         return {'message': 'Invalid amount'}, 400

    #     invoice = LightningInvoice(
    #         user_id=user_id,
    #         amount=amount,
    #         memo=memo,
    #         status='pending',
    #         payment_request='lnbc1...'  # Placeholder, integrate actual LN invoice generation here
    #     )
    #     db.session.add(invoice)
    #     db.session.commit()
    #     return {'invoice_id': invoice.id, 'payment_request': invoice.payment_request}, 201
class LightningInvoiceCheckByHashResource(Resource):
    @jwt_required()
    def get(self, r_hash_hex):
        """
        Check status of a Lightning invoice using r_hash_hex via LND gRPC.
        """
        try:
            invoice = lnd.lookup_invoice(r_hash_str=r_hash_hex)
            return {
                "r_hash_hex": r_hash_hex,
                "memo": invoice.memo,
                "amount_sat": invoice.value,
                "settled": invoice.settled,
                "settle_date": invoice.settle_date
            }, 200
        except Exception as e:
            return {"error": f"Failed to fetch invoice status: {str(e)}"}, 400
        
class LightningInvoiceCheckByIdResource(Resource):

    @jwt_required()
    def get(self, invoice_id):
        user_id = get_jwt_identity()
        invoice = LightningInvoice.query.get(invoice_id)

        if not invoice:
            return {'message': 'Invoice not found'}, 404

        if invoice.user_id != user_id:
            return {'message': 'Access denied'}, 403

        # Fetch real status from LND via r_hash
        try:
            lnd_invoice = lnd.lookup_invoice(r_hash=bytes.fromhex(invoice.r_hash_hex))
        except Exception as e:
            return {'message': f'Error fetching invoice from LND: {str(e)}'}, 500

        # Optionally update local DB status
        if lnd_invoice.settled and invoice.status != 'settled':
            invoice.status = 'settled'
            db.session.commit()

        return {
            'invoice_id': invoice.id,
            'amount': invoice.amount,
            'memo': invoice.memo,
            'status': 'settled' if lnd_invoice.settled else 'pending',
            'payment_request': invoice.payment_request
        }, 200
    # @jwt_required()
    # def get(self, invoice_id):
    #     invoice = LightningInvoice.query.get(invoice_id)
    #     if not invoice:
    #         return {'message': 'Invoice not found'}, 404
    #     user_id = get_jwt_identity()
    #     if invoice.user_id != user_id:
    #         return {'message': 'Access denied'}, 403
    #     return {'status': invoice.status, 'amount': invoice.amount, 'memo': invoice.memo}
    

api.add_resource(LightningInvoiceCreateResource, '/invoice/create')
api.add_resource(LightningInvoiceCheckByHashResource, '/lightning/invoices/<string:r_hash_hex>')
api.add_resource(LightningInvoiceCheckByIdResource, '/invoice/check/<int:invoice_id>')

# --- Transaction Resources ---

# class TransactionListResource(Resource):
#     @jwt_required()
#     def get(self):
#         user_id = get_jwt_identity()
#         transactions = Transaction.query.filter(
#             (Transaction.sender_id == user_id) | (Transaction.receiver_id == user_id)
#         ).all()
#         return {'transactions': [
#             {
#                 'id': t.id,
#                 'amount': t.amount,
#                 'currency': t.currency,
#                 'status': t.status,
#                 'timestamp': t.timestamp.isoformat()
#             } for t in transactions
#         ]}
class TransactionListResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        transactions = Transaction.query.filter(
            (Transaction.sender_id == user_id) | (Transaction.receiver_id == user_id)
        ).all()

        return {'transactions': [
            {
                'id': t.id,
                'sender_id': t.sender_id,
                'receiver_id': t.receiver_id,
                'amount_sats': float(t.amount_sats),
                'amount_fiat': float(t.amount_fiat),
                'status': t.status,
                'created_at': t.created_at.isoformat()
            } for t in transactions
        ]}

class TransactionCreateResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()

        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')
        amount_sats = data.get('amount_sats')
        amount_fiat = data.get('amount_fiat')
        remittance_id = data.get('remittance_id')  # optional

        # Validate required fields
        if not all([sender_id, receiver_id, amount_sats, amount_fiat]):
            return {'message': 'Missing required fields'}, 400

        try:
            transaction = Transaction(
                sender_id=sender_id,
                receiver_id=receiver_id,
                amount_sats=Decimal(str(amount_sats)),
                amount_fiat=Decimal(str(amount_fiat)),
                status='completed',
                remittance_id=remittance_id
            )

            db.session.add(transaction)
            db.session.commit()

            # Fetch sender and receiver from DB
            sender = User.query.get(sender_id)
            receiver = User.query.get(receiver_id)

            # ✅ Async email to sender
            if sender and sender.email:
                send_email(
                    subject="Transaction Sent - Afrilight",
                    recipients=[sender.email],
                    body=(
                        f"Hi {sender.email},\n\n"
                        f"You have successfully sent {amount_sats} sats "
                        f"(approx. ${amount_fiat}) to {receiver.email if receiver else 'your recipient'}.\n"
                        f"Transaction ID: {transaction.id}\n\n"
                        "Thank you for using Afrilight!"
                    )
                )

            # ✅ Async email to receiver
            if receiver and receiver.email:
                send_email(
                    subject="Transaction Received - Afrilight",
                    recipients=[receiver.email],
                    body=(
                        f"Hi {receiver.email},\n\n"
                        f"You have received {amount_sats} sats "
                        f"(approx. ${amount_fiat}) from {sender.email if sender else 'a sender'}.\n"
                        f"Transaction ID: {transaction.id}\n\n"
                        "Thank you for using Afrilight!"
                    )
                )


            # # Send email to sender
            # if sender and sender.email:
            #     msg_sender = Message(
            #         subject="Transaction Sent - Afrilight",
            #         recipients=[sender.email],
            #         body=(
            #             f"Hi {sender.email},\n\n"
            #             f"You have successfully sent {amount_sats} sats "
            #             f"(approx. ${amount_fiat}) to {receiver.email if receiver else 'your recipient'}.\n"
            #             f"Transaction ID: {transaction.id}\n\n"
            #             "Thank you for using Afrilight!"
            #         )
            #     )
            #     mail.send(msg_sender)

            # # Send email to receiver
            # if receiver and receiver.email:
            #     msg_receiver = Message(
            #         subject="Transaction Received - Afrilight",
            #         recipients=[receiver.email],
            #         body=(
            #             f"Hi {receiver.email},\n\n"
            #             f"You have received {amount_sats} sats "
            #             f"(approx. ${amount_fiat}) from {sender.email if sender else 'a sender'}.\n"
            #             f"Transaction ID: {transaction.id}\n\n"
            #             "Thank you for using Afrilight!"
            #         )
            #     )
            #     mail.send(msg_receiver)

            return {
                'message': 'Transaction created successfully',
                'transaction_id': transaction.id
            }, 201

        except Exception as e:
            db.session.rollback()
            return {'message': f'Error creating transaction: {str(e)}'}, 500

class TransactionResource(Resource):
    @jwt_required()
    def get(self, transaction_id):
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return {'message': 'Transaction not found'}, 404

        user_id = get_jwt_identity()
        if user_id not in (transaction.sender_id, transaction.receiver_id):
            return {'message': 'Access denied'}, 403

        return {
            'id': transaction.id,
            'amount_sats': float(transaction.amount_sats),
            'amount_fiat': float(transaction.amount_fiat),
            'status': transaction.status,
            'created_at': transaction.created_at.isoformat()
        }



api.add_resource(TransactionListResource, '/transaction')
api.add_resource(TransactionCreateResource, '/transaction/create')
api.add_resource(TransactionResource, '/transaction/<int:transaction_id>')

# --- PaymentMethod Resources ---

class PaymentMethodListResource(Resource):
    @jwt_required()
    def get(self):
        """List all payment methods, optionally filter by type."""
        method_type = request.args.get("type")
        query = PaymentMethod.query
        if method_type:
            query = query.filter_by(type=method_type)
        methods = query.all()
        return {'payment_methods': [
            {
                'id': m.id,
                'name': m.name,
                'type': m.type,
                'provider_metadata': {
                    'description': m.description
                }
            } for m in methods
        ]}, 200
    

class PaymentMethodCreateResource(Resource):
    @admin_required
    def post(self):
        """Create a new payment method."""
        data = request.get_json()
        name = data.get('name')
        type_ = data.get('type')
        description = data.get('description')

        if not name or not type_:
            return {'message': 'Missing required fields: name and type'}, 400

        pm = PaymentMethod(name=name, type=type_, description=description)
        db.session.add(pm)
        db.session.commit()
        return {'message': 'Payment method created', 'id': pm.id}, 201

class PaymentMethodUpdateDeleteResource(Resource):
    @admin_required
    def put(self, id):
        """Update a payment method by ID."""
        pm = db.session.get(PaymentMethod, id)
        if not pm:
            return {'message': 'Payment method not found'}, 404

        data = request.get_json()
        pm.name = data.get('name', pm.name)
        pm.type = data.get('type', pm.type)
        pm.description = data.get('description', pm.description)
        db.session.commit()
        return {'message': 'Payment method updated'}, 200

    @admin_required
    def delete(self, id):
        """Delete a payment method by ID."""
        pm = db.session.get(PaymentMethod, id)
        if not pm:
            return {'message': 'Payment method not found'}, 404

        db.session.delete(pm)
        db.session.commit()
        return {'message': 'Payment method deleted'}, 200
    

api.add_resource(PaymentMethodListResource, '/payment-methods')
api.add_resource(PaymentMethodCreateResource, '/payment-method')
api.add_resource(PaymentMethodUpdateDeleteResource, '/payment-method/<int:id>')

# --- MobileMoneyProv Resources ---

# class MobileMoneyProvListResource(Resource):
#     @jwt_required()
#     def get(self):
#         providers = MobileMoneyProv.query.all()
#         return {'providers': [
#             {'id': p.id, 'name': p.name, 'country': p.country} for p in providers
#         ]}
    
# api.add_resource(MobileMoneyProvListResource, '/mobile-money/providers')
# List all providers (GET)
class MobileMoneyProvListResource(Resource):
    @jwt_required()
    def get(self):
        providers = MobileMoneyProv.query.all()
        return {'providers': [p.serialize() for p in providers]}, 200

# Create a new provider (POST,PATCH,DELETE)
class MobileMoneyProvResource(Resource):
    @admin_required
    def post(self):
        data = request.get_json()
        if not data or 'provider_name' not in data or 'api_url' not in data:
            return {'message': 'Missing required fields'}, 400

        if MobileMoneyProv.query.filter_by(provider_name=data['provider_name']).first():
            return {'message': 'Provider already exists'}, 409

        new_provider = MobileMoneyProv(
            provider_name=data['provider_name'],
            api_url=data['api_url'],
            country=data.get('country')
        )
        db.session.add(new_provider)
        db.session.commit()
        return {'message': 'Provider created', 'provider': new_provider.serialize()}, 201
    
    @admin_required
    def patch(self, provider_id):
        provider = MobileMoneyProv.query.get(provider_id)
        if not provider:
            return {'message': 'Provider not found'}, 404

        data = request.get_json()
        if not data:
            return {'message': 'No data provided'}, 400

        if 'provider_name' in data:
            provider.provider_name = data['provider_name']
        if 'api_url' in data:
            provider.api_url = data['api_url']
        if 'country' in data:
            provider.country = data['country']

        db.session.commit()
        return {'message': 'Provider updated', 'provider': provider.serialize()}, 200

    @admin_required
    def delete(self, provider_id):
        provider = MobileMoneyProv.query.get(provider_id)
        if not provider:
            return {'message': 'Provider not found'}, 404

        db.session.delete(provider)
        db.session.commit()
        return {'message': 'Provider deleted'}, 200
    
api.add_resource(MobileMoneyProvListResource, '/mobile-money/providers')
api.add_resource(MobileMoneyProvResource, '/mobile-money/providers/create')
# --- ExchangeRate Resources ---

class ExchangeRateResource(Resource):
    def get(self, from_currency, to_currency):
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        # Only support BTC <-> fiat conversions for now
        if from_currency != 'BTC' and to_currency != 'BTC':
            return {'message': 'Only BTC <-> fiat exchange supported'}, 400

        # Case 1: BTC -> fiat
        if from_currency == 'BTC':
            rate = ExchangeRate.query.filter_by(currency_code=to_currency).first()
            if rate:
                return {
                    'from_currency': from_currency,
                    'to_currency': to_currency,
                    'rate': float(rate.btc_to_fiat),
                    'fetched_at': rate.fetched_at.isoformat()
                }
            # fallback to external API
            url = f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies={to_currency.lower()}"
            response = requests.get(url)
            if response.status_code != 200:
                return {'message': 'Failed to fetch external exchange rate'}, 502
            data = response.json()
            if 'bitcoin' not in data or to_currency.lower() not in data['bitcoin']:
                return {'message': 'Exchange rate not found in external API'}, 404
            rate_value = data['bitcoin'][to_currency.lower()]
            return {
                'from_currency': from_currency,
                'to_currency': to_currency,
                'rate': rate_value,
                'fetched_at': None
            }

        # Case 2: fiat -> BTC
        if to_currency == 'BTC':
            rate = ExchangeRate.query.filter_by(currency_code=from_currency).first()
            if rate and rate.btc_to_fiat != 0:
                inverse_rate = 1 / float(rate.btc_to_fiat)
                return {
                    'from_currency': from_currency,
                    'to_currency': to_currency,
                    'rate': inverse_rate,
                    'fetched_at': rate.fetched_at.isoformat()
                }
            # fallback to external API
            url = f"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies={from_currency.lower()}"
            response = requests.get(url)
            if response.status_code != 200:
                return {'message': 'Failed to fetch external exchange rate'}, 502
            data = response.json()
            if 'bitcoin' not in data or from_currency.lower() not in data['bitcoin']:
                return {'message': 'Exchange rate not found in external API'}, 404
            rate_value = data['bitcoin'][from_currency.lower()]
            if rate_value == 0:
                return {'message': 'Invalid rate from external API'}, 502
            return {
                'from_currency': from_currency,
                'to_currency': to_currency,
                'rate': 1 / rate_value,
                'fetched_at': None
            }


api.add_resource(ExchangeRateResource, '/exchange-rate/<string:from_currency>/<string:to_currency>')


# # Start invoice listener thread
# # start_invoice_streamer()
# invoice_streamer = InvoiceStreamer(lnd)
# invoice_streamer.start()


if __name__ == '__main__':
    app.run(debug=True)