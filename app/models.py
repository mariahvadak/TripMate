from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String())
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    def to_json(self):        
        return {"fname": self.first_name,
                "lname": self.last_name,
                "email": self.email}

    def is_authenticated(self):
        return True

    def is_active(self):   
        return True           

    def is_anonymous(self):
        return False          

    def get_id(self):         
        return str(self.id)
        
class Todolist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date())
    title = db.Column(db.String(100))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    todolist= db.Column(db.Integer, db.ForeignKey('todolist.id'))
    date = db.Column(db.String(100))
    text = db.Column(db.String(100))
    complete = db.Column(db.Boolean)