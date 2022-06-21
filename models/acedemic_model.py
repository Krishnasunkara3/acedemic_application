from db import db


class AcedemicModel(db.Model):
    __tablename__ = "acedemicDetails"
    acedemic_details_id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    gained_marks = db.Column(db.Integer, nullable=False)
    student_grade = db.Column(db.String(20), nullable=False)
    total_marks = db.Column(db.Integer, nullable=False, default=600)

    def __init__(self, acedemic_details_id, student_name, gained_marks, student_grade):
        self.acedemic_details_id = acedemic_details_id
        self.student_name = student_name
        self.gained_marks = gained_marks
        self.student_grade = student_grade

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
