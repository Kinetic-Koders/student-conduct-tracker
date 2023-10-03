from App.database import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer, nullable = False, unique = True)
    name = db.Column(db.String, nullable=False)
    karma = db.Column(db.Integer, nullable = True)


    # def __init__(self, id, name, karma):
    #     self.id = id
    #     self.exercise_id = exercise_id
    #     self.name = name

    # get_json function
    def get_json(self):
        return{
            "id":self.id,
            "student_id":self.student_id,
            "name":self.name,
            "karma":self.karma,
        }
