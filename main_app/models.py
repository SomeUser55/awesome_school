
from sqlalchemy import Column, Integer, String
from sqlalchemy_utils import PasswordType, EmailType
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(EmailType)
    password = Column(PasswordType(
            schemes=[
                'pbkdf2_sha512',
                'md5_crypt'
            ],

            deprecated=['md5_crypt']
        ))

    def __repr__(self):
        return "<User(email='%s')>" % (
        self.email)

    def del_user(self):
        pass
