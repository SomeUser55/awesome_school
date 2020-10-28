
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Table, event
from sqlalchemy_utils import PasswordType, EmailType, ChoiceType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

from main_app import db, login

# Base = declarative_base()

user_role_rel = Table('user_role_rel', db.Model.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('role_id', Integer, ForeignKey('role.id'), nullable=False),
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    second_name = db.Column(db.String(32))
    email = db.Column(db.String(32), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # def __repr__(self):
    #     return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    roles = relationship(
        "Role",
        secondary=user_role_rel,
        back_populates="users",
    )


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users = relationship(
        "User",
        secondary=user_role_rel,
        back_populates="roles",
    )
    ROLES_PUBLIC = [
        (u'student', u'Student'),
        (u'mentor', u'Mentor'),
    ]
    ROLES_PRIVATE = [
        (u'admin', u'Admin'),
    ]
    role_type = db.Column(ChoiceType(ROLES_PUBLIC + ROLES_PRIVATE), nullable=False, unique=True)

    def __repr__(self):
        return '<Role {}>'.format(self.role_type)


contest_block_rel = Table('contest_block_rel', db.Model.metadata,
    Column('contest_id', Integer, ForeignKey('contest.id')),
    Column('block_id', Integer, ForeignKey('block.id')),
)


class Contest(db.Model):
    LANGS = [
        (u'python', u'Python'),
    ]
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    desc = db.Column(Text())
    unit_test = db.Column(Text())
    lang = db.Column(ChoiceType(LANGS))
    blocks = relationship(
        "Block",
        secondary=contest_block_rel,
        back_populates="contests")


class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    desc = db.Column(Text())
    contests = relationship(
        "Contest",
        secondary=contest_block_rel,
        back_populates="blocks")


class Submit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(Text())
    contest_id = db.Column(db.Integer, ForeignKey('contest.id'))
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    is_correct = db.Column(db.Boolean())
    create_tstamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
