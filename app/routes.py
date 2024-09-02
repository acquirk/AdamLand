from flask import render_template, request, jsonify, redirect, url_for, flash
from app import app, db
from app.models import Village, Building, Project, Goal
from datetime import datetime

# Main pages
@app.route('/')
def index():
    villages = Village.query.all()
    return render_template('index.html', villages=villages)

@app.route('/kings_castle')
def kings_castle():
    return render_template('kings_castle.html')

# Village routes
@app.route('/village/<int:village_id>')
def view_village(village_id):
    village = Village.query.get_or_404(village_id)
    return render_template('village.html', village=village)

@app.route('/village/add', methods=['GET', 'POST'])
def add_village():
    if request.method == 'POST':
        new_village = Village(
            name=request.form['name'],
            subtitle=request.form['subtitle'],
            advice=request.form['advice']
        )
        db.session.add(new_village)
        db.session.commit()
        flash('Village added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_village.html')

@app.route('/village/<int:village_id>/edit', methods=['GET', 'POST'])
def edit_village(village_id):
    village = Village.query.get_or_404(village_id)
    if request.method == 'POST':
        village.name = request.form['name']
        village.subtitle = request.form['subtitle']
        village.advice = request.form['advice']
        db.session.commit()
        flash('Village updated successfully!', 'success')
        return redirect(url_for('view_village', village_id=village.id))
    return render_template('edit_village.html', village=village)

@app.route('/village/<int:village_id>/delete', methods=['POST'])
def delete_village(village_id):
    village = Village.query.get_or_404(village_id)
    db.session.delete(village)
    db.session.commit()
    flash('Village deleted successfully!', 'success')
    return redirect(url_for('index'))

# Building routes
@app.route('/building/<int:building_id>')
def view_building(building_id):
    building = Building.query.get_or_404(building_id)
    return render_template('building.html', building=building)

@app.route('/village/<int:village_id>/add_building', methods=['GET', 'POST'])
def add_building(village_id):
    villages = Village.query.all()
    current_village = Village.query.get_or_404(village_id)
    if request.method == 'POST':
        new_building = Building(
            name=request.form['name'],
            description=request.form['description'],
            village_id=request.form['village_id']
        )
        db.session.add(new_building)
        db.session.commit()
        flash('Building added successfully!', 'success')
        return redirect(url_for('view_village', village_id=new_building.village_id))
    return render_template('add_building.html', villages=villages, current_village=current_village)

@app.route('/building/<int:building_id>/edit', methods=['GET', 'POST'])
def edit_building(building_id):
    building = Building.query.get_or_404(building_id)
    if request.method == 'POST':
        building.name = request.form['name']
        building.description = request.form['description']
        db.session.commit()
        flash('Building updated successfully!', 'success')
        return redirect(url_for('view_building', building_id=building.id))
    return render_template('edit_building.html', building=building)

@app.route('/building/<int:building_id>/delete', methods=['POST'])
def delete_building(building_id):
    building = Building.query.get_or_404(building_id)
    village_id = building.village_id
    db.session.delete(building)
    db.session.commit()
    flash('Building deleted successfully!', 'success')
    return redirect(url_for('view_village', village_id=village_id))

# Project routes
@app.route('/project/<int:project_id>')
def view_project(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project.html', project=project)

@app.route('/building/<int:building_id>/add_project', methods=['GET', 'POST'])
def add_project(building_id):
    building = Building.query.get_or_404(building_id)
    if request.method == 'POST':
        new_project = Project(
            name=request.form['name'],
            description=request.form['description'],
            building=building
        )
        db.session.add(new_project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('view_building', building_id=building.id))
    return render_template('add_project.html', building=building)

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
    building_id = project.building_id
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('view_building', building_id=building_id))

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

# King's Messenger route
@app.route('/kings_messenger', methods=['GET', 'POST'])
def kings_messenger():
    if request.method == 'POST':
        message = request.form['message']
        # Here you would process the message, perhaps saving it to a database
        # or sending it to another part of the application
        flash('Message sent to the King!', 'success')
        return redirect(url_for('kings_castle'))
    return render_template('kings_messenger.html')

# Error handling routes
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500