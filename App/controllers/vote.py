from App.models import User
from App.database import db

from App.models import Student
from App.models import Review

# create_vote?
# update_vote?

# check if already voted on
def check_voted(review_id, staff_id):
    vote = vote.query.filter_by(review_id=review_id, staff_id=staff_id)

    if voted:
        return True
    return False

# def add_vote(staff_id, review_id, value):

#     exists = check_voted(review_id, staff_id)

#     if exists:


        # existing_vote = cls.query.filter_by(staff_id=staff_id, review_id=review_id).first()

def get_vote(id):
    return Vote.query.filter_by(id=id)

def get_all_votes():
    return Vote.query.all()

def get_all_votes_json():
    votes = Vote.query.all()
    if not votes:
        return []
    votes = [vote.get_json() for vote in votes]
    return votes