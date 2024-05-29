from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()



class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(200), nullable=False)
  description = db.Column(db.String(500), nullable=False)
  date_created = db.Column(db.DateTime, default = datetime.utcnow)

  def __repr__(self) -> str:
    return f"{self.id} - {self.title} - {self.description} - {self.date_created}"

@app.route("/", methods = ['GET', 'POST'])
def home():
  if request.method == 'POST':
    title = request.form['title']
    description = request.form['description']
    todo = Todo(title = title, description = description)
    db.session.add(todo)
    db.session.commit()
  all_todo = Todo.query.all()
  return render_template("index.html", todos = all_todo)

@app.route("/delete/<int:id>")
def delete(id):
  todo = Todo.query.filter_by(id = id).first()
  db.session.delete(todo)
  db.session.commit()
  return redirect("/")

@app.route("/update/<int:id>", methods = ['GET', 'POST'])
def update(id):
  if request.method == 'POST':
    title = request.form['title']
    description = request.form['description']
    todo = Todo.query.filter_by(id = id).first()
    todo.title = title
    todo.description = description
    db.session.add(todo)
    db.session.commit()
    return redirect('/')
  
  todo = Todo.query.filter_by(id = id).first()
  return render_template("update.html", todo = todo)

@app.route('/show/<int:id>')
def show(id):
  todo = Todo.query.filter_by(id = id).first()
  return render_template('show.html', todo = todo)

@app.route('/create', methods = ['GET','POST'])
def create():
  if request.method == 'POST':
    title = request.form['title']
    description = request.form['description']
    todo = Todo(title = title, description = description)
    db.session.add(todo)
    db.session.commit()
    return redirect('/')
  
  return render_template('create.html')

if __name__ == "__main__":
  app.run(debug = True)