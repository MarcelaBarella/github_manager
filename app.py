import os

from flask import (Flask, request, g, session, redirect, url_for,
                   render_template, jsonify, make_response)
from flask_github import GitHub

from infra.database import engine, db_session, Base
from services.github_service import GithubService


app = Flask(__name__)
app.config['GITHUB_CLIENT_ID'] = os.environ.get('GITHUB_CLIENT_ID')
app.config['GITHUB_CLIENT_SECRET'] = os.environ.get('GITHUB_CLIENT_SECRET')
app.config['GITHUB_BASE_URL'] = 'https://api.github.com/'
app.config['GITHUB_AUTH_URL'] = 'https://github.com/login/oauth/'
app.config['DATABASE_URI'] = 'sqlite:////tmp/github-flask.db'

github = GitHub(app)
github_service = GithubService(github, db_session)


def init_db():
    from domain.user import User
    Base.metadata.create_all(bind=engine)


@app.before_request
def before_request():
    access_token = request.cookies.get('user_token')
    if access_token:
        g.user = github_service.update_user_and_get(
            access_token, g)


@app.after_request
def after_request(response):
    db_session.remove()
    return response

@app.route('/index')
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/user', methods=['GET'])
def get_user():
    return jsonify(github.get('/user'))


@app.route('/repos', methods=['GET'])
def get_repos():
    repos = github.get('/user/repos')
    return render_template('repos.html', repos=repos)


@github.access_token_getter
def get_token():
    if 'user' in g:
        return g.user.access_token


@app.route('/github-callback',  methods=['GET'])
@github.authorized_handler
def authorized(oauth_token):
    next_url = request.args.get('next') or url_for('index')
    if oauth_token is None:
        return redirect(next_url)

    github_service.update_user_and_get(oauth_token, g)
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('user_token', oauth_token)
    return resp


@app.route('/login' methods=['GET'])
def login():
    if session.get('user_id', None) is None:
        return github.authorize()
    else:
        return 'Already logged in'


@app.route('/logout', methods=['GET'])
def logout():
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('user_token', '', expires=0)
    return resp


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
