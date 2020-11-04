from celery import Celery

from main_app import db
from main_app.models import User, Contest, Submit, Block, contest_block_rel, Role, Track


app = Celery('tasks', broker='redis://localhost')


@app.task
def check_submit(submit_id):
    print('check_submit')
    submit_obj = Submit.query.get(submit_id)
    contest_obj = Contest.query.get(submit_obj.contest_id)
    total_code = '{0}\n{1}'.format(submit_obj.code, contest_obj.unit_test)
    exec(total_code)
    is_correct = False
    submit_obj.is_correct = is_correct
    db.session.commit()
