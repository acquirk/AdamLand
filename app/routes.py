from flask import render_template, request, jsonify, redirect, url_for, flash
from app import app, db
from app.models import Bucket, Project, Goal
from datetime import datetime

# Main pages
@app.route('/')
def index():
    buckets = Bucket.query.all()
    return render_template('index.html', buckets=buckets)

# Bucket routes
@app.route('/bucket/<int:bucket_id>')
def view_bucket(bucket_id):
    bucket = Bucket.query.get_or_404(bucket_id)
    return render_template('bucket.html', bucket=bucket)

@app.route('/bucket/add', methods=['GET', 'POST'])
def add_bucket():
    if request.method == 'POST':
        new_bucket = Bucket(
            name=request.form['name'],
            subtitle=request.form['subtitle'],
            advice=request.form['advice']
        )
        db.session.add(new_bucket)
        db.session.commit()
        flash('Bucket added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_bucket.html')

@app.route('/bucket/<int:bucket_id>/edit', methods=['GET', 'POST'])
def edit_bucket(bucket_id):
    bucket = Bucket.query.get_or_404(bucket_id)
    if request.method == 'POST':
        bucket.name = request.form['name']
        bucket.subtitle = request.form['subtitle']
        bucket.advice = request.form['advice']
        db.session.commit()
        flash('Bucket updated successfully!', 'success')
        return redirect(url_for('view_bucket', bucket_id=bucket.id))
    return render_template('edit_bucket.html', bucket=bucket)

@app.route('/bucket/<int:bucket_id>/delete', methods=['POST'])
def delete_bucket(bucket_id):
    bucket = Bucket.query.get_or_404(bucket_id)
    db.session.delete(bucket)
    db.session.commit()
    flash('Bucket deleted successfully!', 'success')
    return redirect(url_for('index'))

# Project routes
@app.route('/project/<int:project_id>')
def view_project(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project.html', project=project)

@app.route('/bucket/<int:bucket_id>/add_project', methods=['GET', 'POST'])
def add_project(bucket_id):
    bucket = Bucket.query.get_or_404(bucket_id)
    if request.method == 'POST':
        new_project = Project(
            name=request.form['name'],
            description=request.form['description'],
            bucket=bucket
        )
        db.session.add(new_project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('view_bucket', bucket_id=bucket.id))
    return render_template('add_project.html', bucket=bucket)

@app.route('/project/<int:project_id>/edit', methods=['GET', 'POST'])
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    if request.method == 'POST':
        project.name = request.form['name']
        project.description = request.form['description']
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('view_project', project_id=project.id))
    return render_template('edit_project.html', project=project)

@app.route('/project/<int:project_id>/delete', methods=['POST'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    bucket_id = project.bucket_id
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('view_bucket', bucket_id=bucket_id))

# Goal routes
@app.route('/goal/<int:goal_id>')
def view_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    return render_template('goal.html', goal=goal)

@app.route('/project/<int:project_id>/add_goal', methods=['GET', 'POST'])
def add_goal(project_id):
    project = Project.query.get_or_404(project_id)
    if request.method == 'POST':
        new_goal = Goal(
            description=request.form['description'],
            deadline=datetime.strptime(request.form['deadline'], '%Y-%m-%d'),
            project=project
        )
        db.session.add(new_goal)
        db.session.commit()
        flash('Goal added successfully!', 'success')
        return redirect(url_for('view_project', project_id=project.id))
    return render_template('add_goal.html', project=project)

@app.route('/goal/<int:goal_id>/edit', methods=['GET', 'POST'])
def edit_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if request.method == 'POST':
        goal.description = request.form['description']
        goal.deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%d')
        goal.completed = 'completed' in request.form
        db.session.commit()
        flash('Goal updated successfully!', 'success')
        return redirect(url_for('view_goal', goal_id=goal.id))
    return render_template('edit_goal.html', goal=goal)

@app.route('/goal/<int:goal_id>/delete', methods=['POST'])
def delete_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    project_id = goal.project_id
    db.session.delete(goal)
    db.session.commit()
    flash('Goal deleted successfully!', 'success')
    return redirect(url_for('view_project', project_id=project_id))



# Error handling routes
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500