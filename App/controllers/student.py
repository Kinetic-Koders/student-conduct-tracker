from App.models import Student
from App.database import db

from App.models import Review
from App.models import Vote

# from App.controllers import get_total_votes

# def add_student(student_id, name):
#     newStudent = Student(student_id=student_id, name=name, karma=0)
#     db.session.add(newStudent)
#     db.session.commit()
#     return newStudent

def update_karma(student_id, karma):
    student = get_student(student_id)

    student.karma = karma 
    db.session.add(student)
    db.session.commit()
    return student

# calculate karma
def calc_karma(student_id):
    # import controller here because error if imported at top
    from App.controllers import get_total_votes

    # get all positive and negative reviews for the student
    pos_reviews = Review.query.filter_by(student_id=student_id, positive=True)
    neg_reviews = Review.query.filter_by(student_id=student_id, positive=False)

    
    # if there are no reviews
    if pos_reviews is None and neg_reviews is None:
        print("None")
    #     return 0
    #  do a check for if there are no positive reviews or negative reviews

    # get the difference in values for the positive and negatives
    
    # get all votes for each review and total them, then find difference between number of positive and negative votes
    total_votes = 0
    vote_diff = 0
    for review in pos_reviews:
        # add on the total votes for each review to the total votes of all reviews
        total_votes += get_total_votes(review.id)
        
        #  get number of positive and negative votes for the review
        pos_votes = Vote.query.filter_by(review_id = review.id, value = 1).count()
        neg_votes = Vote.query.filter_by(review_id = review.id, value = -1).count()

        # find the difference between number of positive and negative votes and add it to the total difference
        vote_diff += (pos_votes - neg_votes)

        #  printing for debugging
        print("pos_reviews loop: ", pos_votes, "  ", neg_votes)
        
        # print(vote_diff)
    
    for review in neg_reviews:
        total_votes += get_total_votes(review.id)
        pos_votes = Vote.query.filter_by(review_id = review.id, value = 1).count()
        neg_votes = Vote.query.filter_by(review_id = review.id, value = -1).count()

        # adding difference between negative votes and positive votes here, different than in positive review loops
        vote_diff += (neg_votes - pos_votes)


        #  printing for debugging
        print("neg_reviews loop: ", pos_votes, "  ", neg_votes)
        # print("test")

    #  printing for debugging
    print("total votes = ", total_votes)
    print("vote difference = ", vote_diff, "\n")
    
    #  FIGURE OUT BETTER FORMULA FOR KARMA VALUE

    # karma value is the total difference in votes / total votes
    # so for eg: if 2 posvotes and 1 negvotes, difference is 1
    # then 1 / total (3), for .33

    # original karma formula
    # karma = (vote_diff / total_votes)

    # test formulas
    # this sets the value to a minimum karma of 1 and max of 100, does not account for negative karma 
    # karma = min(max((int(vote_diff / total_votes) + 1) * 100, -100), 100)

    karma = round((vote_diff / total_votes) * 100, 2)

    #  update the karma for the student
    update_karma(student_id, karma)

    return karma
    




# GET KARMA
def get_karma_by_id(student_id):
    student = Student.query.filter_by(student_id=student_id).first()
    if not student:
        return 0
    return student.get_karma()

def get_student(student_id):
    return Student.query.filter_by(student_id=student_id).first()

def get_all_students():
    return Student.query.all()

def get_all_students_json():
    students = Student.query.all()
    if not students:
        return[]
    students = [student.get_json() for student in students]
    return students

    




# def create_exercise(name, description, category):
#     newExercise = Exercise(name=name, description=description, category=category)
#     db.session.add(newExercise)
#     db.session.commit()
#     return newExercise

# def get_exercise_by_name(name):
#     return Exercise.query.filter_by(name=name).first()

# def get_exercise_by_id(id):
#     return Exercise.query.get(id)

# def get_all_exercises():
#     return Exercise.query.all()

# def get_all_exercises_json():
#     exercises = Exercise.query.all()
#     if not exercises:
#         return[]
#     exercises = [exercise.get_json() for exercise in exercises]
#     return exercises