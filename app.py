from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# Replace with a secure secret key
app.config['SECRET_KEY'] = 'your_secret_key'
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
    tasks = Task.query.all()
    form = TaskForm()

    if request.method == 'POST' and form.validate_on_submit():
        new_task = Task(title=form.title.data,
                        description=form.description.data)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('index.html', tasks=tasks, form=form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
