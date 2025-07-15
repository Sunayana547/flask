from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

two = Flask(__name__)
two.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
two.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(two)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"{self.username} {self.password}"

# Step 1: Show form (two.html)
@two.route('/')
def show_form():
    return render_template("two.html")

# Step 2: Form submission → store data → redirect to login page
@two.route('/submit', methods=['POST'])
def submit_form():
    username = request.form['username']
    password = request.form['password']
    todo = Todo(username=username, password=password)
    db.session.add(todo)
    db.session.commit()
    return redirect('/login')

# Step 3: Show login.html with stored data
@two.route('/login')
def show_login_data():
    allTodo = Todo.query.all()
    return render_template('login.html', alltodo=allTodo)
@two.route('/back')
def show_back():
    return render_template("two.html")

@two.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.filter_by(id = id).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return redirect("/login")
    

if __name__ == '__main__':
    with two.app_context():
        db.create_all()
    two.run(debug=True)
