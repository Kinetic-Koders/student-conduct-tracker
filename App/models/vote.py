from App.database import db

from sqlalchemy import CheckConstraint


# maybe not needed?
from sqlalchemy.orm import validates
from App.models import User
from App.models import Review

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    staff_id = db.Column(db.Integer, db.ForeignKey('user.staff_id'), nullable = False)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable = False)

    value = db.Column(db.Integer, nullable = True, server_default = "0" )

    user = db.relationship('User', backref='votes')
    review = db.relationship('Review', backref='votes')

    __table_args__ = (
        CheckConstraint(value.in_([1, 0, -1]), name = 'check_vote_value'),
    )

    def __init__(self, staff_id, review_id, value):
        self.staff_id = staff_id
        self.review_id = review_id
        self.value = value

    def get_json(self):
        return{
            'id': self.id,
            'staff_id': self.staff_id,
            'review_id': self.review_id,
            'self.value': self.value
        }

    #  validates whether or not the staff_id exists in the database
    @validates('staff_id')
    def validate_staff_id(self, key, staff_id):
        # Check if a user with the given staff_id exists
        user = User.query.filter_by(staff_id=staff_id).first()
        if user is None:
            raise ValueError("Invalid staff_id: User does not exist")
        return staff_id

    @validates('review_id')
    def validate_review_id(self, key, review_id):
        # Check if a user with the given staff_id exists
        review = Review.query.filter_by(id=review_id).first()
        if review is None:
            raise ValueError("Invalid review_id: Review does not exist")
        return review_id

    # # Define karma column with server_default constraint
    # karma = db.Column(db.Integer, nullable=True, server_default="2")

    # # Add a check constraint to ensure 'karma' is one of 1, 2, or 3
    # __table_args__ = (
    #     CheckConstraint(karma.in_([1, 2, 3]), name='check_karma_values'),
    # )