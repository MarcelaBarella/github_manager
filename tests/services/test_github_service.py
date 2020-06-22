from mock import MagicMock

import pytest
from flask import g

from services.github_service import GithubService
from app import app


@pytest.fixture(scope='module')
def github():
    github_mock = MagicMock()
    github_mock.__get__ = MagicMock()
    return github_mock

@pytest.fixture(scope='module')
def new_user_github():
    github_mock = MagicMock(id=1981,login='donkeykong', 
                            access_token='pineapplesmells')
    return github_mock

@pytest.fixture(scope='module')
def db_session():
    return MagicMock()

@pytest.fixture(scope='module')
def user():
    return MagicMock(github_id=666, access_token='banana', login='brass_monkey')

@pytest.fixture(scope='module')
def created_new_user():
    return MagicMock(github_id=1981, access_token='pineapplesmells', 
                    login='donkeykong')


class TestGithubService():
    def test_update_user_and_get_authenticate_and_return_user(github, db_session, user):
        with app.app_context():
            github_service = GithubService(github, db_session)
            oauth_token = 'banana'

            assert github_service.update_user_and_get(oauth_token, g) == user


    def test_update_user_and_get_create_user_if_it_not_exists(github, db_session, new_user_gihub, 
                                                            created_new_user):
        with app.app_context():
            github_service = GithubService(github, db_session)
            new_user = github_service.update_user_and_get(new_user_github.access_token, g)

            assert new_user == created_new_user
