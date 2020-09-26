
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
def account():
    return render_template(
        'progress.html',
        title='Progress',
        nav_item_id='progress',
    )