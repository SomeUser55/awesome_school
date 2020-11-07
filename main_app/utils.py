
from functools import wraps

from flask_login import current_user

from main_app import app, login_manager
from main_app.models import EDITORS


def roles_required(*, role_types='ANY'):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()

            if role_types=='ANY' and len(current_user.roles) > 0:
                return fn(*args, **kwargs)

            for role in current_user.roles:
                for r in role_types:
                    if role.role_type == r:
                        return fn(*args, **kwargs)

            return login_manager.unauthorized()

        return decorated_view

    return wrapper


@app.context_processor
def utility_processor():
    def is_editor(user):
        for role in user.roles:
            for r in EDITORS:
                if role.role_type == r:
                    return True

        return False

    return dict(is_editor=is_editor)