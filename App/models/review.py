from App.database import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(120), nullable = True)

    staff_id = db.Column(db.Integer, db.ForeignKey('user.staff_id'))
    # staff = db.relationship('User')

    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'))
    student = db.relationship('Student')

    positive = db.Column(db.Boolean, default = True, nullable = False)

    # add some attribute for the overall karma of the individual review?
    # so that you can total the karma for reviews of a particular student_id
    # then add them up and place into Student object with student_id ????

    def __init__(self, description, staff_id, student_id, positive):
        self.description = description
        self.staff_id = staff_id
        self.student_id = student_id

        self.positive = positive
    
    def __repr__(self):
        return f'<Review {self.id} : {self.description} user {self.user.username}>'

    def get_json(self):
        return{
            'id': self.id,
            'description': self.description,
            'staff_id': self.staff_id,
            'student_id': self.student_id,
            'positive': self.positive
        }
    
    # get positive or not function?
    def get_positive(self):
        return self.positive

    def get_Student_id(self):
        return self.student_id

    # def __init__(self, user_id, exercise_id, name):
    #     self.user_id = user_id
    #     self.exercise_id = exercise_id
    #     self.name = name

    # def __repr__(self):
    #     return f'<ExerciseSet {self.id} : {self.name} user {self.user.username}>'

    # def get_json(self):
    #     return{
    #         'id': self.id,
    #         'name': self.name,
    #         'exercise': self.exercise.name,
    #         'user_id': self.user_id
    #     }



# class ExerciseSet(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'))
#     name = db.Column(db.String, nullable = False)

#     # ???
#     exercise = db.relationship('Exercise')
