from App.models import Vote
from App.database import db

from App.models import Student
from App.models import Review

from App.controllers import get_student_id_from_review, calc_karma

# create_vote?
# update_vote?

# check if already voted on
def check_voted(review_id, staff_id):
    new_vote = Vote.query.filter_by(review_id=review_id, staff_id=staff_id).first()

    return new_vote

def do_vote(staff_id, review_id, value):

    exists = check_voted(review_id, staff_id)
    value = int(value)

    if exists is None:
        new_vote = Vote(staff_id=staff_id, review_id=review_id, value=value)
        db.session.add(new_vote)
        db.session.commit()

        # 
        student_id = get_student_id_from_review(review_id)
        # print(student_id)
        calc_karma(student_id)

        return new_vote
    # can put in an update_vote method ?
    elif exists.value != value:
            print(exists.value, " ", value)
            exists.value = value
            db.session.add(exists)
            db.session.commit()

            # 
            student_id = get_student_id_from_review(review_id)
            calc_karma(student_id)

            return exists
    else:
        db.session.delete(exists)
        db.session.commit()

        # 
        student_id = get_student_id_from_review(review_id)
        calc_karma(student_id)

        return None
    
    # student = get_student_id_from_review(review_id)
    # calc_karma(student.id)

    return 0

def get_total_votes(review_id):
    votes_list = get_all_votes()

    # total = 0

    # for vote in votes_list:
    #     if vote.review_id == review_id:
    #         total += 1

    total = Vote.query.filter_by(review_id=review_id).count()
    
    return total

def get_vote(id):
    return Vote.query.filter_by(id=id).first()

def get_all_votes():
    return Vote.query.all()

def get_all_votes_json():
    votes = Vote.query.all()
    if not votes:
        return []
    votes = [vote.get_json() for vote in votes]
    return votes