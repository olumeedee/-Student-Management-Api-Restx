from ..utils import db

class CourseEnrollment(db.Model):
    __tablename__ = 'course_enrollment'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    percent_grade = db.Column(db.Float(), nullable=False)
    letter_grade = db.Column(db.String(5), nullable=True)

    def __repr__(self):
        return f"<{self.percent_grade}%>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

