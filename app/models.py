# app/models.py
from app import db

class Bucket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    subtitle = db.Column(db.String(128))
    advice = db.Column(db.String(256))
    projects = db.relationship('Project', backref='bucket', lazy='dynamic')

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    bucket_id = db.Column(db.Integer, db.ForeignKey('bucket.id'))
    goals = db.relationship('Goal', backref='project', lazy='dynamic')

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))