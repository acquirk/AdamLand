from flask import render_template, request, jsonify, redirect, url_for
from app import app, db
from app.models import Bucket, Project, Goal
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

@app.route('/')
def index():
    buckets = Bucket.query.all()
    return render_template('index.html', buckets=buckets)

@app.route('/add_project', methods=['POST'])
def add_project():
    try:
        bucket_id = request.json['bucket_id']
        project_name = request.json['project_name'].strip()
        if not project_name:
            return jsonify({'success': False, 'error': 'Project name cannot be empty'}), 400
        project = Project(name=project_name, bucket_id=bucket_id)
        db.session.add(project)
        db.session.commit()
        return jsonify({'success': True, 'project_id': project.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/add_goal', methods=['POST'])
def add_goal():
    try:
        project_id = request.json['project_id']
        goal_description = request.json['goal_description'].strip()
        if not goal_description:
            return jsonify({'success': False, 'error': 'Goal description cannot be empty'}), 400
        goal = Goal(description=goal_description, project_id=project_id)
        db.session.add(goal)
        db.session.commit()
        return jsonify({'success': True, 'goal_id': goal.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/init_buckets')
def init_buckets():
    if Bucket.query.count() == 0:
        buckets = [
            Bucket(name='Internal', subtitle='Nurture your inner self', advice='Self-improvement is a lifelong journey.'),
            Bucket(name='Home', subtitle='Create your sanctuary', advice='A well-organized home leads to a peaceful mind.'),
            Bucket(name='Family', subtitle='Cherish your relationships', advice='Strong bonds are built on communication and shared experiences.'),
            Bucket(name='External', subtitle='Share your gifts with the world', advice='Your unique perspective can make a difference.')
        ]
        db.session.add_all(buckets)
        db.session.commit()
    return redirect(url_for('index'))