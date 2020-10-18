
from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user

from main_app.forms import LoginForm, RegistrationForm, CreateContestForm, SolveContestForm
from main_app import app, db

from main_app.models import User, Contest, Submit


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


@app.route('/courses/<course_name>/<track_name>/<lesson_name>/<block_name>')
def block(course_name, track_name, lesson_name, block_name):
    # theory = teory_dict[]
    return render_template(
        'block.html',
        title=block_name,
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


@app.route('/contests')
@login_required
def contests():
    contests = Contest.query.all()
    return render_template(
        'contests.html',
        title='Contest List',
        contests=contests,
    )


@app.route('/submits')
@login_required
def submits():
    submits = Submit.query.all()

    query = db.session.query(Submit, User, Contest)
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
        form = CreateContestForm()
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
