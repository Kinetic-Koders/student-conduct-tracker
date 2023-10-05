from App.database import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(120), nullable = True)

    staff_id = db.Column(db.Integer, db.ForeignKey('user.staff_id'))

    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'))
    student = db.relationship('Student')

    positive = db.Column(db.Boolean, default = True, nullable = False)

    # not sure if needed?
    # staff = db.relationship('User')

    # add some attribute for the overall karma of the individual review?
    # so that you can total the karma for reviews of a particular student_id
    # then add them up and place into Student object with student_id ????
    
    # upvotes = db.Column(db.Integer, default = 0, nullable = True)
    # downvotes = db.Column(db.Integer, default = 0, nullable = True)

    def __init__(self, description, staff_id, student_id, positive):
        self.description = description
        self.staff_id = staff_id
        self.student_id = student_id

        self.positive = positive

        # self.upvotes = 0
        # self.downvotes = 0
    
    def __repr__(self):
        return f'<Review {self.id} : {self.description} user {self.user.username}>'

    def get_json(self):
        return{
            'id': self.id,
            'description': self.description,
            'staff_id': self.staff_id,
            'student_id': self.student_id,
            'positive': self.positive
            # 'upvotes': self.upvotes,
            # 'downvotes': self.downvotes
        }
    
    # get positive or not function?
    def get_positive(self):
        return self.positive

    def get_Student_id(self):
        return self.student_id

