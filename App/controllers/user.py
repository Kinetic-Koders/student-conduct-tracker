from App.models import User
from App.database import db

from App.models import Student
from App.models import Review

def create_user(username, staff_id, password):
    newuser = User(username=username, staff_id=staff_id, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def log_review(staff_id, student_id, description, positive):
    newReview = Review(staff_id=staff_id, student_id=student_id, description=description, positive=positive)
    db.session.add(newReview)
    db.session.commit()
    return newReview

# FUNCTIONS TO DO:
#   add student, update student, log review, search student

# maybe move to student controllers?
def add_student(student_id, name):
    newStudent = Student(student_id=student_id, name=name, karma=0)
    db.session.add(newStudent)
    db.session.commit()
    return newStudent

# finish this
# def get_all_student_reviews(student_id):
#     student = get_student(student_id)
#     reviews = get_all_reviews()

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
    