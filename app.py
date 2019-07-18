from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(120), nullable=False)
    done = db.Column(db.Boolean, default=False)
    createdAt = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, task, user_id):
        self.task = task
        self.user_id = user_id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    todos = db.relationship('Todo', backref='user', lazy=True)

    def __init__(self, name):
        self.name = name

class TodoSchema(ma.Schema):
    user = ma.Nested("UserSchema", exclude=('todos',))
    class Meta:
        fields = ('id', 'task', 'done', 'createdAt', 'user')

class UserSchema(ma.Schema):
    todos = ma.Nested('TodoSchema', many=True, exclude=('user',))
    class Meta:
        fields = ('id', 'name', 'todos')

todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data['name']
    new_user = User(name)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

@app.route('/user', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)

@app.route('/todo', methods=['POST'])
def add_task():
    data = request.get_json()
    task = data['task']
    user_id = data['user_id']
    new_todo = Todo(task=task, user_id=user_id)
    db.session.add(new_todo)
    db.session.commit()
    return todo_schema.jsonify(new_todo)

@app.route('/todo', methods=['GET'])
def get_all_tasks():
    all_tasks = Todo.query.all()
    result = todos_schema.dump(all_tasks)
    return jsonify(result.data)

@app.route('/todo/<id>', methods=['GET'])
def get_task(id):
    task = Todo.query.get(id)
    if not task:
        return jsonify({"error" : "Not found"}), 404
    return todo_schema.jsonify(task)

@app.route('/todo/<id>', methods=['PUT'])
def update_task(id):
    todo = Todo.query.get(id)
    data = request.get_json()
    task = data['task']
    todo.task = task
    db.session.commit()
    return todo_schema.jsonify(todo)

@app.route('/todo/<id>', methods=['DELETE'])
def delete_task(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return todo_schema.jsonify(todo)

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World'

@app.route('/todo/<id>/done', methods=['POST'])
def set_task_done(id):
    todo = Todo.query.get(id)
    todo.done = True
    db.session.commit()
    return todo_schema.jsonify(todo)

if __name__ == "__main__":
    app.run(debug=True)