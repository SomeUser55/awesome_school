

from flask import request, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user

from main_app.forms import LoginForm, RegistrationForm, CreateContestForm, SolveContestForm, \
    DeleteItemsForm, CreateArrayForm
from main_app import app, db, login_manager
from main_app.models import User, Contest, Submit, Block, contest_block_rel, Role, Track, \
    STUDENT_ROLE, MENTOR_ROLE, ADMIN_ROLE, EDITORS
from .tasks import check_submit
from main_app.utils import roles_required


@app.route('/')
def index_view():
    return render_template(
        "index.html",
        title='Home',
    )


@app.route('/logout')
@roles_required()
def logout_view():
    logout_user()
    return redirect(url_for('index_view'))


@app.route('/account/<user_id>')
@roles_required()
def account_view(user_id):
    user = User.query.get(user_id)
    roles = user.roles
    return render_template(
        'account.html',
        title='Account',
        roles=roles,
    )


@app.route('/register', methods=['GET', 'POST'])
def register_view():
    if current_user.is_authenticated:
        return redirect(url_for('index_view'))

    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
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
        return redirect(url_for('login_view'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_view():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login_view'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('account_view', user_id=user.id))

    return render_template('login.html', title='Sign In', form=form)


@app.route('/block/<block_id>')
@roles_required()
def block_view(block_id):
    block_obj = Block.query.get(block_id)
    return render_template(
        'block.html',
        link_edit=url_for('edit_block_view', block_id=block_id),
        title='Block',
        array=block_obj,
        items=block_obj.contests,
    )


@app.route('/track/<track_id>')
@roles_required()
def track_view(track_id):
    track_obj = Track.query.get(track_id)
    return render_template(
        'track.html',
        link_edit=url_for('edit_track_view', track_id=track_id),
        title='Track',
        array=track_obj,
        items=track_obj.blocks,
    )


@app.route('/contest/<contest_id>', methods=['GET', 'POST'])
@roles_required()
def contest_view(contest_id):
    contest_obj = Contest.query.get(contest_id)
    form = SolveContestForm()

    if request.method == 'POST' and form.validate_on_submit():
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
        check_submit.delay(submit_id)
        return redirect(url_for('contest_view', contest_id=contest_obj.id))

    return render_template(
        'contest.html',
        title='Contest',
        contest=contest_obj,
        form=form,
    )


@app.route('/contests', methods=['GET', 'POST'])
@roles_required()
def contests_view():
    form = DeleteItemsForm()
    contests = Contest.query.all()
    if request.method == 'POST' and form.validate_on_submit():
        for contest_id in form.item_ids.data.split(','):
            Contest.query.filter_by(id=contest_id).delete()

        db.session.commit()

        return redirect(url_for('contests_view'))

    return render_template(
        'contests.html',
        title='Contest List',
        contests=contests,
        form=form,
    )


@app.route('/blocks', methods=['GET', 'POST'])
@roles_required()
def blocks_view():
    form = DeleteItemsForm()
    blocks = Block.query.all()
    if request.method == 'POST' and form.validate_on_submit():
        for block_id in form.item_ids.data.split(','):
            Block.query.filter_by(id=block_id).delete()

        db.session.commit()

        return redirect(url_for('blocks_view'))

    return render_template(
        'blocks.html',
        title='Blocks',
        blocks=blocks,
        form=form,
    )


@app.route('/tracks', methods=['GET', 'POST'])
@roles_required()
def tracks_view():
    form = DeleteItemsForm()
    tracks_list = Track.query.all()
    if request.method == 'POST' and form.validate_on_submit():
        for track_id in form.item_ids.data.split(','):
            Track.query.filter_by(id=track_id).delete()
            db.session.commit()
        return redirect(url_for('tracks_view'))

    return render_template(
        'tracks.html',
        title='Tracks',
        tracks=tracks_list,
        form=form,
    )


@app.route('/submits')
@roles_required()
def submits_view():

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
@roles_required()
def submit_view(submit_id):
    submit_obj = Submit.query.get(submit_id)
    contest_id = submit_obj.__dict__['contest_id']
    contest_obj = Contest.query.get(contest_id)
    return render_template(
        'submit.html',
        title='Submit',
        submit_obj=submit_obj,
        contest_obj=contest_obj,
    )


@app.route('/create_contest', methods=['GET', 'POST'])
@roles_required(role_types=EDITORS)
def create_contest_view():
    form = CreateContestForm()
    if request.method == 'POST' and form.validate_on_submit():
        contest = Contest(
            title=form.title.data,
            desc=form.desc.data,
            unit_test=form.unit_test.data,
            lang=form.lang.data,
        )
        db.session.add(contest)
        db.session.commit()
        return redirect(url_for('contest_view', contest_id=contest.id))
        
        flash('Wrong')

    contests = Contest.query.all()
    return render_template(
        'create_contest.html',
        title='Create',
        contests=contests,
        form=form,
    )


@app.route('/edit_contest/<contest_id>', methods=['GET', 'POST'])
@roles_required(role_types=EDITORS)
def edit_contest_view(contest_id):
    contest_obj = Contest.query.get(contest_id)
    form = CreateContestForm(obj=contest_obj)
    if request.method == 'POST' and form.validate_on_submit():
        contest_obj.title = form.title.data
        contest_obj.desc = form.desc.data
        contest_obj.unit_test = form.unit_test.data
        contest_obj.lang = form.lang.data
        db.session.commit()
        return redirect(url_for('contest_view', contest_id=contest_obj.id))
        
    contests = Contest.query.all()
    return render_template(
        'create_contest.html',
        title='Edit',
        contests=contests,
        form=form,
    )


def create_array(*, form, array_model=None, array_obj=None, item_model, array_items_name):
    if array_obj is None:
        array_obj = array_model(
            title=form.title.data,
            desc=form.desc.data,
        )
    item_ids = [id_ for id_ in form.ids_selected.data.split(',') if id_]
    getattr(array_obj, array_items_name).clear()
    for item_id in item_ids:
        item_obj = item_model.query.get(item_id)
        getattr(array_obj, array_items_name).append(item_obj)
        
    db.session.add(array_obj)
    db.session.commit()


@app.route('/create_block', methods=['GET', 'POST'])
@roles_required(role_types=EDITORS)
def create_block_view():
    form = CreateArrayForm()
    if request.method == 'POST' and form.validate_on_submit():
        create_array(form=form, array_model=Block, item_model=Contest, array_items_name='contests')
        return redirect(url_for('blocks_view'))

    contests = Contest.query.all()
    return render_template(
        'create_block.html',
        title='Create',
        items_to_select=contests,
        items_selected=[],
        form=form,
    )


@app.route('/create_track', methods=['GET', 'POST'])
@roles_required(role_types=EDITORS)
def create_track_view():
    form = CreateArrayForm()
    if request.method == 'POST' and form.validate_on_submit():
        create_array(form=form, array_model=Track, item_model=Block, array_items_name='blocks')
        return redirect(url_for('tracks_view'))

    unused_blocks = Block.query.filter_by(tracks=None)
    return render_template(
        'create_track.html',
        title='Create',
        items_to_select=unused_blocks,
        items_selected=[],
        form=form,
    )


@app.route('/edit_track/<track_id>', methods=['GET', 'POST'])
@roles_required(role_types=EDITORS)
def edit_track_view(track_id):
    track_obj = Track.query.get(track_id)
    form = CreateArrayForm(obj=track_obj)
    if request.method == 'POST' and form.validate_on_submit():
        create_array(form=form, array_obj=track_obj, item_model=Block, array_items_name='blocks')
        return redirect(url_for('track_view', track_id=track_id))

    unused_blocks = Block.query.filter_by(tracks=None)
    return render_template(
        'create_track.html',
        title='Edit',
        items_to_select=unused_blocks,
        items_selected=track_obj.blocks,
        form=form,
    )


@app.route('/edit_block/<block_id>', methods=['GET', 'POST'])
@roles_required(role_types=EDITORS)
def edit_block_view(block_id):
    block_obj = Block.query.get(block_id)
    form = CreateArrayForm(obj=block_obj)
    if request.method == 'POST' and form.validate_on_submit():
        create_array(form=form, array_obj=block_obj, item_model=Contest, array_items_name='contests')
        return redirect(url_for('block_view', block_id=block_obj.id))

    unused_contests = Contest.query.filter_by(blocks=None)
    return render_template(
        'create_block.html',
        title='Edit',
        items_to_select=unused_contests,
        items_selected=block_obj.contests,
        form=form,
    )
