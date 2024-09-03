from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired
from app import app, db, csrf
from app.models import Bucket, Project, Goal, List, ListItem
from datetime import datetime

@app.context_processor
def inject_buckets():
    buckets = Bucket.query.all()
    return dict(buckets=buckets)
def inject_projects():
    projects = Project.query.all()
    return dict(projects=projects)

class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    bucket_id = SelectField('Bucket', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Project')

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
    goal_form = GoalForm()
    list_form = ListForm()
    list_item_form = ListItemForm()
    return render_template('project.html', project=project, goal_form=goal_form, list_form=list_form, list_item_form=list_item_form)

@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    form = ProjectForm()
    form.bucket_id.choices = [(b.id, b.name) for b in Bucket.query.all()]
    
    if form.validate_on_submit():
        new_project = Project(
            name=form.name.data,
            description=form.description.data,
            bucket_id=form.bucket_id.data
        )
        db.session.add(new_project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('view_bucket', bucket_id=new_project.bucket_id))
    
    return render_template('add_project.html', form=form)

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

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired

class GoalForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    deadline = DateField('Deadline', validators=[DataRequired()])
    submit = SubmitField('Add Goal')

class ListForm(FlaskForm):
    name = StringField('List Name', validators=[DataRequired()])
    submit = SubmitField('Add List')

@app.route('/project/<int:project_id>/add_goal', methods=['GET', 'POST'])
def add_goal(project_id):
    project = Project.query.get_or_404(project_id)
    form = GoalForm()
    if form.validate_on_submit():
        new_goal = Goal(
            description=form.description.data,
            deadline=form.deadline.data,
            project=project
        )
        db.session.add(new_goal)
        db.session.commit()
        flash('Goal added successfully!', 'success')
        return redirect(url_for('view_project', project_id=project.id))
    return render_template('project.html', project=project, form=form)

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

# List routes
@app.route('/project/<int:project_id>/add_list', methods=['GET', 'POST'])
def add_list(project_id):
    project = Project.query.get_or_404(project_id)
    form = ListForm()
    if form.validate_on_submit():
        new_list = List(
            name=form.name.data,
            project=project
        )
        db.session.add(new_list)
        db.session.commit()
        flash('List added successfully!', 'success')
        return redirect(url_for('view_project', project_id=project.id))
    return render_template('project.html', project=project, list_form=form, goal_form=GoalForm())

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ListItemForm(FlaskForm):
    content = StringField('New Item', validators=[DataRequired()])
    submit = SubmitField('Add Item')

@app.route('/list/<int:list_id>/add_item', methods=['POST'])
def add_list_item(list_id):
    list_ = List.query.get_or_404(list_id)
    form = ListItemForm()
    if form.validate_on_submit():
        new_item = ListItem(
            content=form.content.data,
            list=list_
        )
        db.session.add(new_item)
        db.session.commit()
        flash('Item added successfully!', 'success')
    return redirect(url_for('view_project', project_id=list_.project_id))

from flask import current_app

@app.route('/list_item/<int:item_id>/toggle', methods=['POST'])
@csrf.exempt
def toggle_list_item(item_id):
    item = ListItem.query.get_or_404(item_id)
    item.completed = not item.completed
    db.session.commit()
    return jsonify({'success': True})

@app.route('/list/<int:list_id>/delete', methods=['POST'])
def delete_list(list_id):
    list_ = List.query.get_or_404(list_id)
    project_id = list_.project_id
    db.session.delete(list_)
    db.session.commit()
    flash('List deleted successfully!', 'success')
    return redirect(url_for('view_project', project_id=project_id))

# Error handling routes
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
