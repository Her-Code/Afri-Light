from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from models.db import db

class User(db.Model, SerializerMixin):

    """User model for storing user information."""
    
    __tablename__ = 'users'

    serialize_rules = ('-password_hash', '-created_at', '-updated_at', '-transactions.user', '-remittances.user', '-payment_methods.user','-transactions.remittance', '-remittances.transactions')

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    other_name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    transactions = db.relationship('Transaction', backref='user', lazy='select')
    remittances = db.relationship('Remittance', backref='user', lazy='select')
    payment_methods = db.relationship('PaymentMethod', backref='user', lazy='select')

    def __repr__(self):
        return f'<User {self.email}>'