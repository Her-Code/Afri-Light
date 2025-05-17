import models.db as db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class ExchangeRate(db.Model, SerializerMixin):
    
    """ExchangeRate model for storing exchange rate information."""

    __tablename__ = 'exchange_rates'

    serialize_rules = ('-payment_method.exchange_rates','-provider.exchange_rates')

    id = db.Column(db.Integer, primary_key=True)
    currency_code = db.Column(db.String(4), nullable=False) 
    btc_to_fiat = db.Column(db.Numeric(10, 8), nullable=False) 
    fetched_at = db.Column(db.DateTime, default=datetime.utcnow)

    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_methods.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('mobile_money_prov.id'), nullable=False)

    payment_method = db.relationship('PaymentMethod',back_populates='exchange_rates',cascade='all, delete-orphan')
    provider = db.relationship(  'MobileMoneyProv',back_populates='exchange_rates',cascade='all, delete-orphan')

    def __repr__(self):
        return f'<ExchangeRate {self.currency_code}>'