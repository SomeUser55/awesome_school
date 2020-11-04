
from functools import wraps

from flask import request, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user  # login_required

from main_app.forms import LoginForm, RegistrationForm, CreateContestForm, SolveContestForm, \
    CreateBlockForm, DeleteContestsForm, DeleteBlocksForm, DeleteTracksForm, \
    CreateTrackForm
from main_app import app, db, login_manager
from main_app.models import User, Contest, Submit, Block, contest_block_rel, Role, Track
from ..tasks import check_submit


STUDENT_ROLE = Role.query.filter_by(role_type='student').first()
MENTOR_ROLE = Role.query.filter_by(role_type='mentor').first()
ADMIN_ROLE = Role.query.filter_by(role_type='admin').first()
EDITOR_GROUP = set([MENTOR_ROLE, ADMIN_ROLE])

# MENTOR_ROLE = "MENTOR_ROLE"


def roles_required(*, roles='ANY'):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                # print('if not current_user.is_authenticated')
                return login_manager.unauthorized()

            if roles=='ANY' and len(current_user.roles) > 0:
                # print("f roles=='ANY' and len(current_user.roles) > 0")
                return fn(*args, **kwargs)

            if set(roles).issubset(set(current_user.roles)):
                # print('if set(roles).issubset(set(current_user.roles))')
                return fn(*args, **kwargs)

            # print('return login_manager.unauthorized()')
            return login_manager.unauthorized()

        return decorated_view

    return wrapper


@app.context_processor
def utility_processor():
    def is_editor(user):
        # return EDITOR_GROUP.issubset(set(user.roles))
        # return MENTOR_ROLE in user.roles
        # print('user.roles', user.roles, type(user.roles))
        # print('MENTOR_ROLE', MENTOR_ROLE, type(MENTOR_ROLE))
        # return user.roles[0].role_type == MENTOR_ROLE 
        return True

    return dict(is_editor=is_editor)


@app.route('/')
def index():
    return render_template(
        "index.html",
        title='Home',
        # mycontent="Welcome to Awesome School!",
    )


@app.route('/progress/')
# @login_required
def progress():
    return render_template(
        'progress.html',
        title='Progress',
        not_done='true'
    )


@app.route('/logout')
# @login_required
@roles_required()
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/account/<user_id>')
# @login_required
@roles_required()
def account(user_id):
    user = User.query.get(user_id)
    roles = user.roles
    return render_template(
        'account.html',
        title='Account',
        roles=roles,
    )


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        role_obj = Role.query.filter_by(role_type=form.role.data).first()

        user = User(
            first_name=form.first_name.data,
            second_name=form.second_name.data,
            email=form.email.data,
            roles=[role_obj],
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('account', user_id=current_user.id))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('account', user_id=user.id))

    return render_template('login.html', title='Sign In', form=form)


@app.route('/block/<block_id>')
# @login_required
@roles_required()
def block(block_id):
    block_obj = Block.query.get(block_id)
    print("block_obj.contests", block_obj.contests)
    return render_template(
        'block.html',
        title='Block',
        block=block_obj,
        contests=block_obj.contests,
    )


@app.route('/track/<track_id>')
# @login_required
@roles_required()
def track(track_id):
    track_obj = Track.query.get(track_id)
    return render_template(
        'track.html',
        title='Track',
        track=track_obj,
        blocks=track_obj.blocks,
    )


@app.route('/webinar')
# @login_required
@roles_required()
def webinar():
    return render_template(
        'webinar.html',
        title='Webinar',
    )


@app.route('/contest/<contest_id>', methods=['GET', 'POST'])
# @login_required
@roles_required()
def contest(contest_id):
    contest_obj = Contest.query.get(contest_id)
    form = SolveContestForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            # is_correct = True
            submit = Submit(
                code=form.code.data,
                contest_id=contest_id,
                user_id=current_user.id,
                # is_correct=is_correct,
            )
            db.session.add(submit)
            db.session.commit()
            submit_id = submit.id
            print('submit_id', submit_id)
            check_submit.delay(submit_id)
            flash('Code submited')
            return redirect(url_for('contest', contest_id=contest_obj.id))

    return render_template(
        'contest.html',
        title='Contest',
        contest=contest_obj,
        form=form,
    )


@app.route('/contests', methods=['GET', 'POST'])
# @login_required
@roles_required()
def contests():
    form = DeleteContestsForm()
    contests = Contest.query.all()
    if request.method == 'POST':
        if form.validate_on_submit():
            for contest_id in form.contest_ids.data.split(','):
                print(contest_id)
                Contest.query.filter_by(id=contest_id).delete()

            db.session.commit()

        return redirect(url_for('contests'))

    return render_template(
        'contests.html',
        title='Contest List',
        contests=contests,
        form=form,
    )


@app.route('/blocks', methods=['GET', 'POST'])
# @login_required
@roles_required()
def blocks():
    form = DeleteBlocksForm()
    blocks = Block.query.all()
    if request.method == 'POST':
        if form.validate_on_submit():
            for block_id in form.block_ids.data.split(','):
                Block.query.filter_by(id=block_id).delete()

            db.session.commit()

        return redirect(url_for('blocks'))

    return render_template(
        'blocks.html',
        title='Blocks',
        blocks=blocks,
        form=form,
    )


@app.route('/tracks', methods=['GET', 'POST'])
# @login_required
@roles_required()
def tracks():
    form = DeleteTracksForm()
    tracks_list = Track.query.all()
    if request.method == 'POST' and form.validate_on_submit():
        print("if request.method == 'POST' and form.validate_on_submit():")
        for track_id in form.track_ids.data.split(','):
            Track.query.filter_by(id=track_id).delete()
            db.session.commit()
        return redirect(url_for('tracks'))

    return render_template(
        'tracks.html',
        title='Tracks',
        tracks=tracks_list,
        form=form,
    )


@app.route('/submits')
# @login_required
@roles_required()
def submits():

    

    query = db.session.query(Submit, User, Contest)\
        .join(User, User.id==Submit.user_id)\
            .join(Contest, Contest.id==Submit.contest_id)
    records = query.all()



    return render_template(
        'submits.html',
        title='Submit List',
        records=records,
    )


@app.route('/submit/<submit_id>')
# @login_required
@roles_required()
def submit(submit_id):
    submit_obj = Submit.query.get(submit_id)
    contest_id = submit_obj.__dict__['contest_id']
    contest_obj = Contest.query.get(contest_id)
    return render_template(
        'submit.html',
        title='Submit',
        submit_obj=submit_obj,
        contest_obj=contest_obj,
    )


@app.route('/create', methods=['GET', 'POST'])
@roles_required()
def create():
    form = CreateContestForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            contest = Contest(
                title=form.title.data,
                desc=form.desc.data,
                unit_test=form.unit_test.data,
                lang=form.lang.data,
            )
            db.session.add(contest)
            db.session.commit()
            flash('Contest created')
            return redirect(url_for('contest', contest_id=contest.id))
        
        flash('Wrong')

    contests = Contest.query.all()
    return render_template(
        'create.html',
        title='Create',
        contests=contests,
        form=form,
    )


@app.route('/edit/<contest_id>', methods=['GET', 'POST'])
# @login_required
@roles_required()
def edit(contest_id):
    contest_obj = Contest.query.get(contest_id)
    form = CreateContestForm(obj=contest_obj)
    if request.method == 'POST':
        if form.validate_on_submit():
            contest_obj.title = form.title.data
            contest_obj.desc = form.desc.data
            contest_obj.unit_test = form.unit_test.data
            contest_obj.lang = form.lang.data

            db.session.commit()
            flash('Contest edited')
            return redirect(url_for('contest', contest_id=contest_obj.id))
        
        flash('Wrong')

    contests = Contest.query.all()
    return render_template(
        'create.html',
        title='Edit',
        contests=contests,
        form=form,
    )


@app.route('/edit_block/<block_id>', methods=['GET', 'POST'])
# @login_required
@roles_required()
def edit_block(block_id):
    block_obj = Block.query.get(block_id)
    form = CreateBlockForm(obj=block_obj)
    if request.method == 'POST':
        if form.validate_on_submit():
            block_obj.title = form.title.data
            block_obj.desc = form.desc.data

            contests_list = []
            contest_ids = [id_ for id_ in form.contest_ids.data.split(',') if id_]
            for contest_id in contest_ids:
                contest_obj = Contest.query.get(contest_id)
                contests_list.append(contest_obj)

            print('contest_ids', contest_ids)
            block_obj.contests = contests_list

            db.session.commit()
            flash('Contest edited')
            return redirect(url_for('block', block_id=block_obj.id))
        
        flash('Wrong')

    unused_contests = Contest.query.filter_by(blocks=None)
    return render_template(
        'create_block.html',
        title='Edit',
        unused_contests=unused_contests,
        block_contests=block_obj.contests,
        form=form,
    )


@app.route('/edit_track/<track_id>', methods=['GET', 'POST'])
# @login_required
@roles_required(roles=EDITOR_GROUP)
def edit_track(track_id):
    track_obj = Track.query.get(track_id)
    form = CreateTrackForm(obj=track_obj)
    if request.method == 'POST' and form.validate_on_submit():
        track_obj.title = form.title.data
        track_obj.desc = form.desc.data

        blocks_list = []
        block_ids = [id_ for id_ in form.block_ids.data.split(',') if id_]
        for block_id in block_ids:
            block_obj = Block.query.get(block_id)
            blocks_list.append(block_obj)

        print('blocks_list', blocks_list)
        track_obj.blocks = blocks_list

        db.session.commit()
        return redirect(url_for('track', track_id=track_id))
        
        flash('Wrong')

    unused_blocks = Block.query.filter_by(tracks=None)
    return render_template(
        'create_track.html',
        title='Edit',
        unused_blocks=unused_blocks,
        used_blocks=track_obj.blocks,
        form=form,
    )


@app.route('/create_block', methods=['GET', 'POST'])
# @login_required
@roles_required()
def create_block():
    form = CreateBlockForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            block_obj = Block(
                title=form.title.data,
                desc=form.desc.data,
            )

            contest_ids = [id_ for id_ in form.contest_ids.data.split(',') if id_]
            print("contest_ids", contest_ids)
            for contest_id in contest_ids:
                contest_obj = Contest.query.get(contest_id)
                block_obj.contests.append(contest_obj)

            db.session.add(block_obj)
            db.session.commit()
            flash('Block created')
            return redirect(url_for('blocks'))
    
    contests = Contest.query.all()
    return render_template(
        'create_block.html',
        title='Create',
        unused_contests=contests,
        block_contests=[],
        form=form,
    )


@app.route('/create_track', methods=['GET', 'POST'])
# @login_required
@roles_required(roles=EDITOR_GROUP)
def create_track():
    form = CreateTrackForm()
    if request.method == 'POST' and form.validate_on_submit():
        print("if request.method == 'POST' and form.validate_on_submit()")
        track_obj = Track(
            title=form.title.data,
            desc=form.desc.data,
        )

        block_ids = [id_ for id_ in form.block_ids.data.split(',') if id_]
        for block_id in block_ids:
            print('block_id', block_id)
            block_obj = Block.query.get(block_id)
            track_obj.blocks.append(block_obj)

            db.session.add(track_obj)
            db.session.commit()
        return redirect(url_for('tracks'))

    blocks_list = Block.query.all()
    return render_template(
        'create_track.html',
        title='Create',
        unused_blocks=blocks_list,
        used_blocks=[],
        form=form,
    )
