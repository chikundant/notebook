from flask_login import UserMixin
from project import login
from project.db import MySQLUser
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin):
    id = 0
    username = None
    email = None
    remember_me = False
    password_hash = None

    def load(self, id):
        db = MySQLUser()
        info = db.get_by_field('*', 'id', id)
        if info:
            self.id = info[0]
            self.username = info[1]
            self.email = info[2]
            self.password_hash = info[3]
        return self

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_none(self):
        if self.username is None or self.password_hash is None:
            return True
        else:
            return False

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    user = User()
    user.load(int(id))
    return user
