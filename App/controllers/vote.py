from App.models import Vote
from App.database import db

from App.models import Student
from App.models import Review

# create_vote?
# update_vote?

# check if already voted on
def check_voted(review_id, staff_id):
    new_vote = Vote.query.filter_by(review_id=review_id, staff_id=staff_id).first()

    return new_vote

def do_vote(staff_id, review_id, value):

    exists = check_voted(review_id, staff_id)

    if exists is None:
        new_vote = Vote(staff_id=staff_id, review_id=review_id, value=value)
        db.session.add(new_vote)
        db.session.commit()
        return new_vote
    # can put in an update_vote method
    elif exists.value != value:
            exists.value = value
            db.session.add(exists)
            db.session.commit()
            return exists
    else:
        db.session.delete(exists)
        db.session.commit()
        return None
    return None

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