from App.models import User
from App.database import db

from App.models import Student

def create_user(username, staff_id, password):
    newuser = User(username=username, staff_id=staff_id, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

# FUNCTIONS TO DO:
#   add student, update student, log review, search student

def add_student(student_id, name):
    newStudent = Student(student_id=student_id, name=name, karma=0)
    db.session.add(newStudent)
    db.session.commit()
    return newStudent


# def update_student(student_id, karma):


# def add_student(student_id, name):
#     newStudent = Student(student_id=student_id, name=name, karma=0)
#     db.session.add(newStudent)
#     db.session.commit()
#     return newStudent

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def get_user_by_staffid(staff_id):
    return User.query.filter_by(staff_id=staff_id).first()


def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    