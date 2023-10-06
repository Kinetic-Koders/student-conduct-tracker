from App.database import db

from sqlalchemy import CheckConstraint

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    #  maybe dont need staff_id since review_id has it
    staff_id = db.Column(db.Integer, db.ForeignKey('user.staff_id'), nullable = False)
    review_id = db.Column(db.Integer, db.ForeignKey('review.staff_id'), nullable = False)

    value = db.Column(db.Integer, nullable = True, server_default = "0" )

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

    # # Define karma column with server_default constraint
    # karma = db.Column(db.Integer, nullable=True, server_default="2")

    # # Add a check constraint to ensure 'karma' is one of 1, 2, or 3
    # __table_args__ = (
    #     CheckConstraint(karma.in_([1, 2, 3]), name='check_karma_values'),
    # )