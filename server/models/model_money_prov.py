import models.db as db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class MobileMoneyProv(db.Model, SerializerMixin):

    """MobileMoneyProvider model for storing mobile money provider information."""
    
    __tablename__ = 'mobile_money_prov'
    serialize_rules = ('-created_at', '-updated_at','-payment_methods.provider', '-exchange_rates.provider')

    id = db.Column(db.Integer, primary_key=True)
    provider_name = db.Column(db.String(100), nullable=False)
    api_url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    payment_methods = db.relationship('payment_methods', backref='provider', lazy='select')
    exchange_rate = db.relationship('ExchangeRate', backref='provider', lazy='select')

    def __repr__(self):
        return f'<MobileMoneyProvider {self.provider_name}>'