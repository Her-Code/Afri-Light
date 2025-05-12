from models.db import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class Escrow(db.Model, SerializerMixin):
    """Escrow model for storing escrow information."""

    __tablename__ = 'escrow'
    serialize_rules = ('-created_at', '-updated_at', '-remittance.escrow')

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), nullable=False) 
    release_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    remittance_id = db.Column(db.Integer, db.ForeignKey('remittance.id'), nullable=False)

    remittance = db.relationship('Remittance', back_populates='escrow')

    def __repr__(self):
        return f'<Escrow {self.id}>'
