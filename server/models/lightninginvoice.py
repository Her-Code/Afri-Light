import models.db as db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class LightningInvoice(db.Model, SerializerMixin):
    """LightningInvoice model for storing Lightning invoice information."""

    __tablename__ = 'lightning_invoices'
    serialize_rules = ('-created_at', '-updated_at', '-remittance.lightning_invoice')

    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'), nullable=False)
    invoice = db.Column(db.String(255), nullable=False)
    amount_btc = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), nullable=False) 
    expiration_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    remittance_id = db.Column(db.Integer, db.ForeignKey('remittance.id'), nullable=False)
    
    remittance = db.relationship('Remittance', back_populates='lightning_invoice')
    wallet = db.relationship('Wallet', back_populates='lightning_invoices')

    def __repr__(self):
        return f'<LightningInvoice {self.id}>'