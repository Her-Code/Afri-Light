import models.db as db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class PaymentMethod(db.Model, SerializerMixin):

    """PaymentMethod model for storing payment method information."""
    
    __tablename__ = 'payment_methods'
    serialize_rules = ( '-created_at', '-updated_at','-remittances.payment_method', '-exchange_rates.payment_method', '-provider.payment_methods')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('mobile_money_prov.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    provider = db.relationship('mobile_money_prov', back_populates='payment_methods')
    remittances = db.relationship('Remittance', back_populates='payment_method', cascade='all, delete-orphan')
    exchange_rates = db.relationship('ExchangeRate', back_populates='payment_method',cascade='all, delete-orphan')

    def __repr__(self):
        return f'<PaymentMethod {self.name}>'