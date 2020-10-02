
from sqlalchemy import Column, Integer, String, PasswordType, EmailType

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    password = Column(PasswordType(
            schemes=[
                'pbkdf2_sha512',
                'md5_crypt'
            ],

            deprecated=['md5_crypt']
        ))
    email = Column(EmailType)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
        self.name, self.fullname, self.nickname)