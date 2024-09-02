from app import db
from datetime import datetime

class Village(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    subtitle = db.Column(db.String(128))
    advice = db.Column(db.String(256))
    buildings = db.relationship('Building', backref='village', lazy='dynamic')

class Building(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(256))
    village_id = db.Column(db.Integer, db.ForeignKey('village.id'))
    projects = db.relationship('Project', backref='building', lazy='dynamic')

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(256))
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'))
    goals = db.relationship('Goal', backref='project', lazy='dynamic')

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256))
    deadline = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))