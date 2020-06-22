from unittest.mock import MagicMock, Mock, patch

import pytest
from assertpy import assert_that

from services.github_service import GithubService
from domain.user import User


@pytest.fixture
def github():
    github_mock = Mock()
    github_mock.get.return_value = {
        'id': 'github_foo_user_id',
        'login': 'github_foo_login',
        'repos_url': 'https://api.github.com/foo_repos_url'
    }

    return github_mock


@pytest.fixture
def github_service(github, db_session):
    return GithubService(github, db_session)


@pytest.fixture
def db_session():
    return Mock()


@pytest.fixture
def flask_global():
    return Mock()


@pytest.fixture
def updated_user(github_service, flask_global):
    user = github_service.update_user_and_get('foo_token', flask_global)
    return user


def test__update_user_and_get__should_set_user_access_token(updated_user):
    assert_that(updated_user.access_token).is_equal_to('foo_token')


def test__update_user_and_get__should_set_github_id(updated_user):
    assert_that(updated_user.github_id).is_equal_to('github_foo_user_id')


def test__update_user_and_get__should_set_login(updated_user):
    assert_that(updated_user.login).is_equal_to('github_foo_login')


def test__update_user_and_get__should_set_repos_url(updated_user):
    assert_that(updated_user.repos_url).is_equal_to(
        'https://api.github.com/foo_repos_url')


def test__update_user_and_get__should_get_user_data_from_github(updated_user, github):
    github.get.assert_called_once()
