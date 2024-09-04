from app import db
from datetime import datetime

class Bucket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    subtitle = db.Column(db.String(128))
    advice = db.Column(db.String(256))
    projects = db.relationship('Project', backref='bucket', lazy='dynamic')
    inbox_items = db.relationship('InboxItem', backref='bucket', lazy='dynamic')

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(256))
    bucket_id = db.Column(db.Integer, db.ForeignKey('bucket.id'))
    goals = db.relationship('Goal', backref='project', lazy='dynamic')
    lists = db.relationship('List', backref='project', lazy='dynamic')
    archived = db.Column(db.Boolean, default=False)

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256))
    deadline = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    items = db.relationship('ListItem', backref='list', lazy='dynamic')

class ListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(256))
    completed = db.Column(db.Boolean, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))

class InboxItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bucket_id = db.Column(db.Integer, db.ForeignKey('bucket.id'), nullable=True)
