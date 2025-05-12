from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource,Api
from models.db import db
from models.user import User
# from models.transaction import Transaction
# from models.wallet import Wallet
# from models.remittance import Remittance
# from models.exchange_rate import ExchangeRate
# from models.lightninginvoice import LightningInvoice
# from models.escrow import Escrow
# from models.payment_method import PaymentMethod
# from models.mobile_money_prov import MobileMoneyProv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///afrilight.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
api = Api(app)

with app.app_context():
    db.create_all()
    # Initialize the database and create tables
    # db.create_all()
    # Add initial data if needed
    # user = User(username='admin', password=bcrypt.generate_password_hash('password').decode('utf-8'))
    # db.session.add(user)
    # db.session.commit()

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

if __name__ == '__main__':
    app.run(debug=True)