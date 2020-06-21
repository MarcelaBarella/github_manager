from domain.user import User


class GithubService:
    def __init__(self, github, db_session):
        self.github = github
        self.db_session = db_session

    def update_user_and_get(self, github_token, flask_global):
        request_user = User()
        request_user.access_token = github_token

        flask_global.user = request_user
        github_user = self.github.get('/user')
        github_id = github_user['id']

        user = User.query.filter_by(github_id=github_id).first()
        if user is None:
            user = User()
            user.github_id = github_id
            user.login = github_user['login']
            user.repos_url = github_user['repos_url']
            self.db_session.add(user)

        user.access_token = github_token
        self.db_session.commit()

        return user
