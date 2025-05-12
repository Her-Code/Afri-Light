import models.db as db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class Wallet(db.Model, SerializerMixin):
    """Wallet model for storing wallet information."""

    __tablename__ = 'wallet'
    serialize_rules = ('-created_at', '-updated_at', '-user.wallets')

    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    wallet_address = db.Column(db.String(255), nullable=False)
    currency_code = db.Column(db.String(4), nullable=False) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='wallets')
    lightning_invoices = db.relationship('LightningInvoice', back_populates='wallet', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Wallet {self.id}>'