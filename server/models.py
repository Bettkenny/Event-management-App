from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)

    organized_events = db.relationship('Event', backref='organizer', lazy=True)
    tickets = db.relationship('Ticket', backref='user', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    tickets = db.relationship('Ticket', backref='event', lazy=True)

    __table_args__ = (
        db.Index('idx_event_date', 'date'),
    )

    def calculate_total_revenue(self):
        return sum(ticket.total_cost for ticket in self.tickets)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)

    @validates('quantity')
    def validate_quantity(self, key, value):
        if value <= 0:
            raise ValueError('Quantity must be greater than 0.')
        return value
