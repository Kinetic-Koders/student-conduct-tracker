from App.database import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer, nullable = False, unique = True)
    name = db.Column(db.String, nullable=False)
    karma = db.Column(db.Integer, nullable = True)

    # exercise = db.relationship('ExerciseSet', backref = 'user')
    

    # this was commented off the whole time, not sure why
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.karma = 0



    # get_json function
    def get_json(self):
        return{
            "id":self.id,
            "student_id":self.student_id,
            "name":self.name,
            "karma":self.karma,
        }

    # get karma score function?
    def get_karma(self):
        return self.karma

    