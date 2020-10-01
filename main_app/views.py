
from flask import request, render_template

from main_app import app
from main_app import db


@app.route('/')
def index_view():
    return render_template(
        "index.html",
        title='Home',
        nav_item_id='home',
        # mycontent="Welcome to Awesome School!",
    )


@app.route('/progress')
def progress_view():
    return render_template(
        'progress.html',
        title='Progress',
        nav_item_id='progress',
        not_done='true'
    )


@app.route('/account')
def account_view():
    return render_template(
        'account.html',
        title='Account',
        nav_item_id='account',
    )


@app.route('/login')
def login_view():
    return render_template(
        'login.html',
        title='Login',
        nav_item_id='login',
    )


@app.route('/register')
def register_view():
    return render_template(
        'register.html',
        title='Register',
        nav_item_id='register',
    )


@app.route('/courses')
def courses_view():
    links = []
    for course_id, course_info in db.courses_dict.items():
        name = course_info['title']
        links.append({
            'name': name,
            'href': f"/course/{course_id}"
        })

    return render_template(
        'courses.html',
        title='Courses',
        nav_item_id='courses',
        links=links,
    )


@app.route('/course/<course_id>')
def course_view(course_id):

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
        nav_item_id='courses',
        links=track_links,
    )


@app.route('/track/<track_id>')
def track_view(track_id):
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
        nav_item_id='courses',
        links=lesson_links,
        desc=desc,
    )


@app.route('/lesson/<lesson_id>')
def lesson_view(lesson_id):
    lesson = db.lessons_dict[lesson_id]
    title = lesson['title']
    return render_template(
        'lesson.html',
        title=title,
        nav_item_id='courses',
        )


@app.route('/courses/<course_name>/<track_name>/<lesson_name>/<block_name>')
def block_view(course_name, track_name, lesson_name, block_name):
    # theory = teory_dict[]
    return render_template(
        'block.html',
        title=block_name,
        nav_item_id='block',
    )


@app.route('/webinar')
def webinar_view():
    return render_template(
        'webinar.html',
        title='Webinar',
        nav_item_id='webinar',
    )

