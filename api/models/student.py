from .users import User
from ..utils import db

class Student(User):
    __tablename__ = 'students'
    enrollments = db.relationship('CourseEnrollment', backref='student', lazy=True)

    def __repr__(self):
        return f"<Student {self.first_name} {self.last_name}>"
    
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
    

    
