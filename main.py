from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Farhan#2020@localhost/task_manager'
db = SQLAlchemy(app)


class Task(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable = False)
    description = db.Column(db.Text)
    is_complete = db.Column(db.Boolean,default = False)
    


if __name__ == '__main__':
    # This command reads your classes and actually builds the tables in MySQL!
    with app.app_context():
        db.create_all() 
    
    app.run(debug=True)