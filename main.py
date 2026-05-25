from flask import Flask,session,render_template,request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)
app.secret_key = "farhan"

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),nullable = False, unique = True)
    password = db.Column(db.String(50),nullable= False)
    
    tasks = db.relationship('Task', backref='owner', lazy=True)


class Task(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable = False)
    description = db.Column(db.Text)
    is_complete = db.Column(db.Boolean,default = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/register/<username>/<password>')
def register(username,password):

    existing_user = User.query.filter_by(username=username).first()

    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, password=hashed_pw)

    db.session.add(new_user)
    db.session.commit()

    return f"{username} registered"

@app.route('/login',methods =['GET','POST'])
def login():

    if request.method == 'Post':

        form_username = request.form['username']
        form_password = request.form['password']

        user = User.query.filer_by(username = form_username).first()

        if not user:
            return "error: user not found login first"
    
        if check_password_hash(user.password,form_password):
            session['user_id'] = user.id
            return f"welcome back {user.username}"
        else:
            return "incorrect password!"
        
    return render_template('login.html')

@app.route('/add')
def add_task():
    
    if 'user_id' not in session:
        return "Access denied: Please login first"
    
    current_user_id = session['user_id']
    user = User.query.get(current_user_id)

    my_task = Task(title="hello", description="first row", user_id= current_user_id)
    my_task2 = Task(title="my", description="second row",user_id =  current_user_id)
    my_task3 = Task(title="people", description="third row", user_id= current_user_id)

    db.session.add(my_task)
    db.session.add(my_task2)
    db.session.add(my_task3)
    db.session.commit()

    return f"Tasks successfully created and assigned to {user.username}!"

@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get(id)

    if not task:
        return f"Error: Task {id} does not exist! (Maybe it was already deleted?)"

    db.session.delete(task)
    db.session.commit()

    return f"{id} deleted"

@app.route('/complete/<int:id>')
def update(id):
    task = Task.query.get(id)

    task.is_complete = True

    db.session.commit()

    return f"task {id} has been marked completed"




@app.route('/')
def view_tasks():

    if 'user_id' not in session:
        return "Access denied: Please login first"
    
    current_user_id = session['user_id']

    user_task = Task.query.filter_by(user_id=current_user_id).all()


    tasks_list = []
    for task in user_task:
        tasks_list.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        })
    return {"tasks": tasks_list}


@app.route('/logout')
def logout():
    session.pop('user_id',None)
    return "you have been logged out"

    


if __name__ == '__main__':
    # This command reads your classes and actually builds the tables in MySQL!
    with app.app_context():
        db.create_all() 
    
    app.run(debug=True)