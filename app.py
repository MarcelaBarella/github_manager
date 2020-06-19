from flask import (Flask, request, g, session, redirect, url_for,
                    render_template ,jsonify, render_template_string)
from flask_github import GitHub
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


app = Flask(__name__)
app.config['GITHUB_CLIENT_ID'] = 'f0859156c46db4e5ed5d'
app.config['GITHUB_CLIENT_SECRET'] = 'adc3ec6ca59afcd825e87a7fd24118b07c41dfb0'
app.config['GITHUB_BASE_URL'] = 'https://api.github.com'
app.config['GITHUB_AUTH_URL'] = 'https://github.com/login/oauth/'
app.config['DATABASE_URI'] =  'sqlite:////tmp/github.db'

github = GitHub(app)

engine = create_engine(app.config['DATABASE_URI'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    access_token = Column(String(255))
    github_id = Column(Integer)
    login = Column(String(255))

    def __init__(self, access_token):
        self.ccess_token = access_token


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@app.after_request
def after_request(response):
    db_session.remove()
    return response


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')



@github.access_token_getter
def get_token():
    user = g.user
    if user is not None:
        return user.access_token


@app.route('/github-callback')
@github.authorized_handler
def authorized(access_token):
    next_url = request.args.get('next') or url_for('index')
    if access_token is None:
        return redirect(next_url)

    user = User.query.filter_by(access_token=access_token).first()
    if user is None:
        user = User(access_token)
        db_session.add(user)

    user.access_token = access_token

    g.user = user
    github_user = github.get('/user')
    user.github_id = github_user['id']
    user.login = github_user['login']

    db_session.commit()

    session['user_id'] = user.id
    return redirect(next_url)


@app.route('/login')
def login():
    if session.get('user_id', None) is None:
        return github.authorize()
    else:
        return 'Already logged in'


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/user')
def get_user():
    return jsonify(github.get('/user'))


@app.route('/repo')
def get_repo():
    return jsonify(github.get(''))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
