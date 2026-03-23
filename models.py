from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.LargeBinary, nullable=False)
    records = db.relationship('StudyRecord', backref='student', lazy=True)

class StudyRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject_name = db.Column(db.String(100), nullable=False)
    study_hours = db.Column(db.Integer, nullable=False)
    attendance = db.Column(db.Integer, nullable=False)
    previous_score = db.Column(db.Integer, nullable=False)
    predicted_score = db.Column(db.Integer, nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    suggestion = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
