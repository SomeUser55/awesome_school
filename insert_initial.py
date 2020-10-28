

from main_app.models import Role
from main_app import db

roles_list = [
    u'student',
    u'mentor',
    u'admin',
]

for role_type_ in roles_list:
    some = Role.query.filter_by(role_type=role_type_).first()
    print(some)
    if not some:
        print('inserting', role_type_)
        obj = Role(role_type=role_type_)
        db.session.add(obj)

db.session.commit()

rows = Role.query.all()
print(rows)
