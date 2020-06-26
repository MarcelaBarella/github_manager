from domain.repository import Repository

class ReposService:
    def __init__(self, repository, db_session):
        self.repository = repository
        self.db_session = db_session
        # self.tags = tags

    def update_repo_and_get(self):
        repo = Repository()
        repo.user_id = repository['owner']['id']
        repo.repo_id = repository['id']
        repo.description = repository['description']
        repo.url = repository['url']

