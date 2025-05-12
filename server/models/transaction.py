import models.db as db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class Transaction(db.Model, SerializerMixin):

    """Transaction model for storing transaction information."""
    
    __tablename__ = 'transactions'

    serialize_rules = ('-sender_id', '-remittance_id', '-created_at', '-updated_at', '-remittance.transactions', '-sender.transactions','-remittance.exchange_rate')

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    remittance_id = db.Column(db.Integer, db.ForeignKey('remittances.id'), nullable=False)
    receiver_name = db.Column(db.String(100), nullable=False)
    receiver_phone = db.Column(db.String(20), nullable=False)
    amount_btc = db.Column(db.Numeric(10, 8), nullable=False)
    amount_fiat = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    remittance = db.relationship('Remittance', backref='transactions', lazy='select')
    sender = db.relationship('User', backref='transactions', lazy='select')

    def __repr__(self):
        return f'<Transaction {self.id}>'