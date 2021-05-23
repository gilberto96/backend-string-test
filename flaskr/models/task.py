from ..database import db;
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Task(db.Model, SerializerMixin):
    __tablename__ = "tasks"

    serialize_only = ('id', 'title','description','start_date', 'due_date', "priority")

    id = db.Column(db.Integer(),primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.DateTime(), nullable=False)
    due_date = db.Column(db.DateTime(), nullable=False)
    priority = db.Column(db.Integer(), nullable=False)

    assignee_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    assignee_user = relationship("User", back_populates="tasks")
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.current_timestamp())

    def save(self):
        try:
                db.session.add(self)
                db.session.commit()
                return self
        except Exception as e:
                print(e)
                return False

    def get_single(id, assignee_user_id = None):
        query = Task.query.filter_by(id=id)
        if assignee_user_id is not None:
            query = query.filter_by(assignee_user_id=assignee_user_id)
        
        return query.first()

    def get_all():
        return Task.query.all()

    def delete(self):
        try:
                db.session.delete(self)
                db.session.commit()
                return True
        except:
                return False