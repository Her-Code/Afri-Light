import models.db as db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class Remittance(db.Model, SerializerMixin):
    """Remittance model for storing remittance information."""
    __tablename__ = 'remittances'

    serialize_rules = ('-sender_id', 'payment_method_id', '-created_at', '-updated_at', '-transactions.remittance', '-payment_method.remittances', '-exchange_rate.remittance')

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_name = db.Column(db.String(100), nullable=False)
    receiver_phone = db.Column(db.String(20), nullable=False)
    amount_btc = db.Column(db.Numeric(10, 8), nullable=False)
    amount_fiat = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_methods.id'), nullable=False)
    receiver_currency = db.Column(db.String(4), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sender = db.relationship('User', backref='remittances', lazy='select')
    payment_method = db.relationship('PaymentMethod', backref='remittances', lazy='select')
    transactions = db.relationship('Transaction', backref='remittance', lazy='select')
    exchange_rate = db.relationship('ExchangeRate', backref='remittance', lazy='select')

    def __repr__(self):
        return f'<Remittance {self.id}>'