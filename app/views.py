from flask import request, render_template, redirect, flash, url_for, abort
from app.forms import LoginForm, SignUpForm, CreateTaskForm
from app import app, login_manager, db
from app.models import User, Task
from flask_login import login_required, current_user, login_user, logout_user
import datetime


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup/', methods=["get", "post"])
def create_account():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(email = form.email.data,
                    name=form.name.data,
                    gender=bool(int(form.gender.data)))
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect('/')
    return render_template('signup.html',form=form)

@app.route('/login/', methods=['get', 'post'])
def login():
    form = LoginForm()
    errors = []
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            errors.append('Неверный логин или пароль')
    return render_template('login.html', form=form, errors=errors)

@app.route('/tasks/')
@login_required
def user_tasks():
    tasks = current_user.tasks
    param_filter = request.args.get('filter')
    if param_filter:
        is_done = True if param_filter == 'completed' else False
        tasks = db.session.query(Task).filter(Task.user==current_user, Task.done==is_done).all()
    return render_template('tasks.html', tasks=tasks, now=datetime.datetime.now())

@app.route('/tasks/<int:id>/', methods=['POST', 'DELETE'])
@login_required
def update_task_status(id: int):
    task = db.session.query(Task).get(id)
    if not task:
        abort(404)
    if task.user != current_user:
        abort(403)
    if request.method == 'DELETE':
        db.session.query(Task).filter(Task.id==id).delete()
    else:
        task.set_done()
        db.session.add(task)
    db.session.commit()
    return (f"{request.method} SUCCESS", 200)

@app.route('/create_task/', methods=['get', 'post'])
@login_required
def create_task():
    form = CreateTaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, description=form.description.data, user=current_user)
        db.session.add(task)
        db.session.commit()
        flash('Задача успешно добавлена')
        return redirect('/create_task/')
    return render_template('create_task.html', form=form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('home'))
