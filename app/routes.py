# app/routes.py
from flask import render_template, request, jsonify
from app import app, db
from app.models import Bucket, Project, Goal

@app.route('/')
def index():
    buckets = Bucket.query.all()
    return render_template('index.html', buckets=buckets)

@app.route('/add_project', methods=['POST'])
def add_project():
    bucket_id = request.json['bucket_id']
    project_name = request.json['project_name']
    project = Project(name=project_name, bucket_id=bucket_id)
    db.session.add(project)
    db.session.commit()
    return jsonify({'success': True, 'project_id': project.id})

@app.route('/add_goal', methods=['POST'])
def add_goal():
    project_id = request.json['project_id']
    goal_description = request.json['goal_description']
    goal = Goal(description=goal_description, project_id=project_id)
    db.session.add(goal)
    db.session.commit()
    return jsonify({'success': True, 'goal_id': goal.id})