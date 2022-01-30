from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
# from models import Todo
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return str(self.name)


@app.route('/')
def home():
    if request.method == 'POST':
        name = request.form['name']
        new_task = Todo(name=name)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
    else:

        tasks = Todo.query.order_by(Todo.created_at)
    context = {
        tasks: tasks
    }

    return render_template('home.html', context=context)


@app.route('/delete/<int:id>')
def delete(id):
    task = Todo.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        db.redirect('/')
    except Exception:
        return 'An Error occur during deleting data'


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):

    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/')
        except Exception:
            return 'An Error occur during updating data'
    else:
        title = 'update task'
        context = {
            title: title,
            task: task,
        }
        return render_template('update.html', context=context)


if __name__ == '__main__':
    app.run(debug=True)
