
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Table
from sqlalchemy_utils import PasswordType, EmailType, ChoiceType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

from main_app import db, login

# Base = declarative_base()

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
