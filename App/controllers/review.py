from App.models import Review
from App.database import db

from App.models import Student
# ???
from App.controllers import *

# def create_review(staff_id, student_id, description, positive):
#     newReview = Review(staff_id=staff_id, student_id=student_id, description=description, positive=positive)
#     db.session.add(newReview)
#     db.session.commit()
#     return newReview

def get_review(id):
    review = Review.query.filter_by(id=id).first()

def get_all_reviews():
    return Review.query.all()

def get_all_reviews_json():
    reviews = Review.query.all()
    if not reviews:
        return []
    reviews = [review.get_json() for review in reviews]
    return reviews





# def update_review(id, description, positive):
#     review = get_review(id)
#     if review:
#         review.description = description
#         review.positive = positive
#         db.session.add(review)
#         return db.session.commit()
#     return None

# def get_all_users_json():
#     users = User.query.all()
#     if not users:
#         return []
#     users = [user.get_json() for user in users]
#     return users

# def update_user(id, username):
#     user = get_user(id)
#     if user:
#         user.username = username
#         db.session.add(user)
#         return db.session.commit()
#     return None
