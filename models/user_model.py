from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from api.index import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    nama = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_authenticated_admin(self):
        return self.is_authenticated and self.is_admin

    def __repr__(self):
        return f'<User {self.username}>'