from app import db
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),nullable=False)
    name = db.Column(db.String(20),nullable=False)
    password = db.Column(db.String(20),nullable=False)
    gender = db.Column(db.Boolean,nullable=False)

class Info(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    salary = db.Column(db.Float,nullable=False)
    age = db.Column(db.SmallInteger,nullable=False)