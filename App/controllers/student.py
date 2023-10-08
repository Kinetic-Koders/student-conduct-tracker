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
    from App.controllers import get_total_votes
    # get all positive and negative reviews for a student
    pos_reviews = Review.query.filter_by(student_id=student_id, positive=True)
    neg_reviews = Review.query.filter_by(student_id=student_id, positive=False)

    

    if pos_reviews is None and neg_reviews is None:
        print("Noneee")
    #     return 0

    # print(neg_reviews)
    # get the difference in values for the positive and negatives
    
    # get all votes for each review and total them, then find difference
    total_votes = 0
    vote_diff = 0
    for review in pos_reviews:
        total_votes += get_total_votes(review.id)
        
        pos_votes = Vote.query.filter_by(review_id = review.id, value = 1).count()
        neg_votes = Vote.query.filter_by(review_id = review.id, value = -1).count()

        print("pos_reviews loop: ", pos_votes, "  ", neg_votes)
        vote_diff += (pos_votes - neg_votes)
        


        # get total number of votes for that review
        # get the difference in upvotes for it
        # print(vote_diff)
    
    for review in neg_reviews:
        pos_votes = Vote.query.filter_by(review_id = review.id, value = 1).count()
        neg_votes = Vote.query.filter_by(review_id = review.id, value = -1).count()

        print("neg_reviews loop: ", pos_votes, "  ", neg_votes)
        vote_diff += (neg_votes - pos_votes)
        # print("test")

    print("total votes = ", total_votes)
    print("vote difference = ", vote_diff, "\n")
    
    karma = (vote_diff / total_votes)
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