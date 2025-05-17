import models.db as db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class Remittance(db.Model, SerializerMixin):
    """Remittance model for storing remittance information."""
    __tablename__ = 'remittances'

    serialize_rules = ( '-created_at', '-updated_at', '-sender.sent_remittances', '-receiver.received_remittances', '-escrow.remittance', '-lightning_invoice.remittance','-transactions.remittance', '-payment_method.remittances')

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_name = db.Column(db.String(100), nullable=False)
    receiver_phone = db.Column(db.String(20), nullable=False)
    amount_sats = db.Column(db.BigInteger, nullable=False)
    amount_fiat = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_methods.id'), nullable=False)
    receiver_currency = db.Column(db.String(4), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    preferred_payout_currency = db.Column(db.String(4), nullable=True) 

    sender = db.relationship('User',foreign_keys=[sender_id], back_populates='remittances')
    receiver = db.relationship('User',foreign_keys=[receiver_id], back_populates='received_remittances')
    payment_method = db.relationship('PaymentMethod', back_populates='remittances')
    transactions = db.relationship('Transaction', back_populates='remittance')
    escrow = db.relationship('Escrow', back_populates='remittance',  cascade='all, delete-orphan')
    lightning_invoice = db.relationship('LightningInvoice', back_populates='remittance', cascade='all, delete-orphan')


    def __repr__(self):
        return f'<Remittance {self.id}>'