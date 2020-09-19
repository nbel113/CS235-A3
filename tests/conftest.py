import os
import pytest

from movie_web_app import create_app
from movie_web_app.a_adapters import memory_repository
from movie_web_app.a_adapters.memory_repository import MemoryRepository
from movie_web_app.a_blueprints import movies

TEST_DATA_PATH = os.path.join('C:', os.sep, 'Users', 'nigel', 'Desktop', 'University Work',
                              'Year 3 (2020)', 'Semester 2', 'CompSci 235', '235 assignments',
                              '235 A2', 'CS235-A2', 'tests', 'data')

@pytest.fixture
def movies_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH, repo)
    return repo

@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,                                # Set to True during testing.
        'TEST_DATA_PATH': TEST_DATA_PATH,               # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False                       # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()