from ..database import db;
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import load_only, relationship
from werkzeug.security import check_password_hash
from sqlalchemy import Table, Column, Integer, ForeignKey

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    serialize_only = ('id', 'email','fullname','photo', 'created_at','password')

    id = db.Column(db.Integer(),primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(500), nullable=False)
    fullname = db.Column(db.String(50), nullable=False)
    photo = db.Column(db.String(255), nullable=True)
    tasks = relationship("Task", back_populates="assignee_user")
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.current_timestamp())

    def authenticate(email, password):
        user = User.query.filter_by(email=email).first()
        print(f"________________authenticate__________")
        
        if user is None or not check_password_hash(user.password,password):
            return None
        else:
            return user

    def identity(payload):
        print("________________identity__________")
        user_id = payload["identity"]
        user = User.query.filter_by(id=user_id).first()
        return user

    def get_by_id(id):
        return User.query.filter_by(id=id).first()

    def get_all():
        return User.query.all()

    def save(self):
        try:
                db.session.add(self)
                db.session.commit()
                return self
        except Exception as e:
                print(e)
                return False

    def delete(self):
        try:
                db.session.delete(self)
                db.session.commit()
                return True
        except:
                return False