
from flask import request, render_template

from main_app import app


@app.route('/')
def index():
    return render_template(
        "index.html",
        title='Home',
        nav_item_id='home',
        # mycontent="Welcome to Awesome School!",
    )


@app.route('/progress')
def progress():
    return render_template(
        'progress.html',
        title='Progress',
        nav_item_id='progress',
    )


@app.route('/account')
def account():
    return render_template(
        'account.html',
        title='Account',
        nav_item_id='account',
    )


@app.route('/lesson')
def lesson():
    return render_template(
        'lesson.html',
        title='Lesson',
        nav_item_id='lesson',
    )


@app.route('/login')
def login():
    return render_template(
        'login.html',
        title='Login',
        nav_item_id='login',
    )


@app.route('/register')
def register():
    return render_template(
        'register.html',
        title='Register',
        nav_item_id='register',
    )


@app.route('/courses')
def courses():
    links = [
        {'name': 'Go', 'href': '/courses/golang'},
        {'name': 'F#', 'href': '/courses/f_sharp'},
        {'name': 'Python', 'href': '/courses/python'},
    ]
    return render_template(
        'courses.html',
        title='Courses',
        nav_item_id='courses',
        links=links,
    )


@app.route('/courses/<course_name>')
def course(course_name):
    desc_dict = {
        'golang': '''Go is a statically typed, compiled programming language
            designed at Google[14] by Robert Griesemer, Rob Pike, and Ken Thompson''',
        'f_sharp': '''F# (pronounced F sharp) is a functional-first,
            general purpose, strongly typed, multi-paradigm programming language
            that encompasses functional, imperative, and object-oriented programming methods.''',
        'python': '''Python is an interpreted, high-level and general-purpose programming language.
            Created by Guido van Rossum and first released in 1991,
            Python's design philosophy emphasizes code readability with its notable use of significant whitespace.''',
    }
    track_dicts = {
        'python': [
            {'name': 'beginer', 'href': '/courses/python/beginer'},
            {'name': 'medium', 'href': '/courses/python/medium'},
            {'name': 'hard', 'href': '/courses/python/hard'},
        ]
    }
    desc = desc_dict[course_name]
    tracks = track_dicts.get(course_name, [])
    return render_template(
        'course.html',
        title=course_name,
        desc=desc,
        nav_item_id='course',
        tracks=tracks,
    )


@app.route('/courses/<course_name>/<track_name>')
def track(course_name, track_name):
    return render_template(
        'track.html',
        title='{}: {}'.format(course_name, track_name),
        nav_item_id='track',
    )


@app.route('/webinar')
def webinar():
    return render_template(
        'webinar.html',
        title='Webinar',
        nav_item_id='webinar',
    )


@app.route('/block')
def block():
    return render_template(
        'block.html',
        title='Block',
        nav_item_id='block',
    )
