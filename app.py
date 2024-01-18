from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# Replace with a secure secret key
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)


class TaskForm(FlaskForm):
    title = StringField('Title', render_kw={
                        "placeholder": "Task title"}, validators=[DataRequired()])
    description = TextAreaField('Description', render_kw={
                                "placeholder": "Task description"})
    submit = SubmitField('Add Task')


@app.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 3  # Adjust this number based on your preference
    tasks = Task.query.paginate(page=page, per_page=per_page)
    form = TaskForm()

    if request.method == 'POST' and form.validate_on_submit():
        new_task = Task(title=form.title.data,
                        description=form.description.data)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully', 'success')
        return redirect(url_for('index'))

    return render_template('index.html', tasks=tasks, form=form)


@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    form = TaskForm()

    if request.method == 'POST' and form.validate_on_submit():
        new_task = Task(title=form.title.data,
                        description=form.description.data)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully', 'success')
        return redirect(url_for('index'))

    return render_template('add_task.html', form=form)


@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully', 'success')
    return redirect(url_for('index'))


@app.route('/update_task/<int:task_id>', methods=['POST', 'GET'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm()

    if request.method == 'POST' and form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        db.session.commit()
        flash('Task updated successfully', 'success')
        return redirect(url_for('index'))

    return render_template('update_task.html', task=task, form=form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
