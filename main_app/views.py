
from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user

from main_app.forms import LoginForm, RegistrationForm, CreateContestForm, SolveContestForm, CreateBlockForm, DeleteContestsForm, DeleteBlocksForm
from main_app import app, db

from main_app.models import User, Contest, Submit, Block, contest_block_rel


@app.route('/')
def index():
    return render_template(
        "index.html",
        title='Home',
        # mycontent="Welcome to Awesome School!",
    )


@app.route('/progress/')
@login_required
def progress():
    return render_template(
        'progress.html',
        title='Progress',
        not_done='true'
    )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/account/<user_id>')
@login_required
def account(user_id):
    return render_template(
        'account.html',
        title='Account',
    )


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            second_name=form.second_name.data,
            email=form.email.data,
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


@app.route('/courses')
def courses():
    links = []
    # for course_id, course_info in db.courses_dict.items():
    #     name = course_info['title']
    #     links.append({
    #         'name': name,
    #         'href': f"/course/{course_id}"
    #     })

    return render_template(
        'courses.html',
        title='Courses',
        links=links,
    )


@app.route('/course/<course_id>')
def course(course_id):

    course = db.courses_dict[course_id]
    track_ids = course['track_ids']

    track_links = []
    for track_id in track_ids:
        track = db.tracks_dict[track_id]
        name = track['title']
        track_links.append({
            'name': name,
            'href': f"/track/{track_id}"
        })

    title = course['title']
    desc = course['desc']
    return render_template(
        'course.html',
        title=title,
        desc=desc,
        links=track_links,
    )


@app.route('/track/<track_id>')
def track(track_id):
    track = db.tracks_dict[track_id]
    lesson_ids = track['lesson_ids']

    lesson_links = []
    for lesson_id in lesson_ids:
        lesson = db.lessons_dict[lesson_id]
        name = lesson['title']
        lesson_links.append({
            'name': name,
            'href': f"/lesson/{lesson_id}",
        })

    title = track['title']
    desc = track['desc']
    return render_template(
        'track.html',
        title=title,
        links=lesson_links,
        desc=desc,
    )


@app.route('/lesson/<lesson_id>')
def lesson(lesson_id):
    lesson = db.lessons_dict[lesson_id]
    title = lesson['title']
    return render_template(
        'lesson.html',
        title=title,
        )


@app.route('/block/<block_id>')
@login_required
def block(block_id):
    block_obj = Block.query.get(block_id)
    print("block_obj.contests", block_obj.contests)
    return render_template(
        'block.html',
        title='Block',
        block=block_obj,
        contests=block_obj.contests,
    )


@app.route('/webinar')
@login_required
def webinar():
    return render_template(
        'webinar.html',
        title='Webinar',
    )


@app.route('/contest/<contest_id>', methods=['GET', 'POST'])
@login_required
def contest(contest_id):
    contest_obj = Contest.query.get(contest_id)
    print(contest_obj.blocks)
    form = SolveContestForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            is_correct = True
            submit = Submit(
                code=form.code.data,
                contest_id=contest_id,
                user_id=current_user.id,
                is_correct=is_correct,
            )
            db.session.add(submit)
            db.session.commit()
            flash('Code submited')
            return redirect(url_for('contest', contest_id=contest_obj.id))

    return render_template(
        'contest.html',
        title='Contest',
        contest=contest_obj,
        form=form,
    )


@app.route('/contests', methods=['GET', 'POST'])
@login_required
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
@login_required
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


@app.route('/submits')
@login_required
def submits():
    submits = Submit.query.all()

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
@login_required
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
@login_required
def create():
    form = CreateContestForm()

    if request.method == 'POST':
        # form = CreateContestForm()
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
@login_required
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
@login_required
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


            rels = contest_block_rel.query.all()
            print(rels)


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



@app.route('/create_block', methods=['GET', 'POST'])
@login_required
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


# @app.route('/delete', methods=['GET', 'POST'])
# @login_required
# def delete():
    
#     return render_template(
#         'create_block.html',
#         title='Create',
#         contests=contests,
#         form=form,
#     )