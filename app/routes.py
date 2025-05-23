from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired
from app import app, db, csrf
from app.models import Bucket, Project, Goal, List, ListItem, InboxItem
from flask import jsonify

@app.route('/archive/<string:item_type>/<int:item_id>', methods=['POST'])
def archive_item(item_type, item_id):
    archive_bucket = Bucket.query.filter_by(name="Archive").first()
    if not archive_bucket:
        return jsonify({"success": False, "error": "Archive bucket not found"}), 404

    if item_type == 'project':
        item = Project.query.get_or_404(item_id)
        item.bucket_id = archive_bucket.id
    elif item_type == 'goal':
        item = Goal.query.get_or_404(item_id)
        item.project.bucket_id = archive_bucket.id
    elif item_type == 'list':
        item = List.query.get_or_404(item_id)
        item.project.bucket_id = archive_bucket.id
    elif item_type == 'inbox':
        item = InboxItem.query.get_or_404(item_id)
        item.bucket_id = archive_bucket.id
    else:
        return jsonify({"success": False, "error": "Invalid item type"}), 400

    db.session.commit()
    return jsonify({"success": True})
from datetime import datetime

@app.context_processor
def inject_buckets():
    buckets = Bucket.query.all()
    archive_bucket = Bucket.query.filter_by(name="Archive").first()
    return dict(buckets=buckets, archive_bucket=archive_bucket)
def inject_projects():
    projects = Project.query.all()
    return dict(projects=projects)

class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    bucket_id = SelectField('Bucket', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Project')

class InboxItemForm(FlaskForm):
    content = StringField('New Idea', validators=[DataRequired()])
    submit = SubmitField('Add to Inbox')

# Main pages
@app.route('/')
def index():
    buckets = Bucket.query.all()
    for bucket in buckets:
        bucket.projects = Project.query.filter_by(bucket_id=bucket.id).all()
    inbox_items = InboxItem.query.filter_by(bucket_id=None).all()
    inbox_form = InboxItemForm()
    assign_form = FlaskForm()  # Create a new form for CSRF protection
    return render_template('index.html', buckets=buckets, inbox_items=inbox_items, inbox_form=inbox_form, form=assign_form)

# Bucket routes
@app.route('/bucket/<int:bucket_id>')
def view_bucket(bucket_id):
    bucket = Bucket.query.get_or_404(bucket_id)
    inbox_items = InboxItem.query.filter_by(bucket_id=bucket_id).all()
    form = FlaskForm()  # Create a new form for CSRF protection
    return render_template('bucket.html', bucket=bucket, inbox_items=inbox_items, form=form)

@app.route('/add_inbox_item', methods=['POST'])
def add_inbox_item():
    form = InboxItemForm()
    if form.validate_on_submit():
        destination = request.form.get('destination', '')
        new_item = InboxItem(content=form.content.data)
        
        if destination.startswith('bucket_'):
            bucket_id = int(destination.split('_')[1])
            new_item.bucket_id = bucket_id
            flash('New idea added to bucket!', 'success')
        elif destination.startswith('project_'):
            project_id = int(destination.split('_')[1])
            project = Project.query.get(project_id)
            if project:
                new_goal = Goal(description=form.content.data, project=project)
                db.session.add(new_goal)
                flash('New idea added as a goal to the project!', 'success')
            else:
                flash('Project not found.', 'error')
                return redirect(url_for('index'))
        else:
            flash('New idea added to inbox!', 'success')
        
        db.session.add(new_item)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/assign_inbox_item/<int:item_id>', methods=['POST'])
def assign_inbox_item(item_id):
    form = FlaskForm()
    if form.validate_on_submit():
        item = InboxItem.query.get_or_404(item_id)
        bucket_id = request.form.get('bucket_id')
        if bucket_id:
            item.bucket_id = bucket_id
            db.session.commit()
            flash('Idea assigned to bucket!', 'success')
    else:
        flash('Invalid form submission.', 'error')
    return redirect(url_for('index'))

@app.route('/assign_inbox_item_to_project/<int:item_id>', methods=['POST'])
def assign_inbox_item_to_project(item_id):
    form = FlaskForm()
    if form.validate_on_submit():
        item = InboxItem.query.get_or_404(item_id)
        project_id = request.form.get('project_id')
        if project_id:
            project = Project.query.get_or_404(project_id)
            # Create a new Goal from the InboxItem
            new_goal = Goal(
                description=item.content,
                project=project
            )
            db.session.add(new_goal)
            db.session.delete(item)  # Remove the item from the inbox
            db.session.commit()
            flash('Inbox item assigned to project as a new goal!', 'success')
        else:
            flash('Invalid project selection.', 'error')
    else:
        flash('Invalid form submission.', 'error')
    return redirect(url_for('view_bucket', bucket_id=item.bucket_id))

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

@app.route('/project/<int:project_id>/archive', methods=['POST'])
def archive_project(project_id):
    project = Project.query.get_or_404(project_id)
    project.archived = True
    db.session.commit()
    flash('Project archived successfully!', 'success')
    return redirect(url_for('view_bucket', bucket_id=project.bucket_id))

@app.route('/project/<int:project_id>/unarchive', methods=['POST'])
def unarchive_project(project_id):
    project = Project.query.get_or_404(project_id)
    project.archived = False
    db.session.commit()
    flash('Project unarchived successfully!', 'success')
    return redirect(url_for('view_bucket', bucket_id=project.bucket_id))

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
        return redirect(url_for('view_project', project_id=goal.project_id))
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
