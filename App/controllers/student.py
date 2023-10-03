from App.models import Student
from App.database import db

# def add_student(student_id, name):
#     newStudent = Student(student_id=student_id, name=name, karma=0)
#     db.session.add(newStudent)
#     db.session.commit()
#     return newStudent

# GET KARMA

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