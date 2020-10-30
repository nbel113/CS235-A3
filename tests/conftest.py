import os
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from movie_web_app import create_app
from movie_web_app.a_adapters import memory_repository, database_repository
from movie_web_app.a_adapters.orm import metadata, map_model_to_tables
from movie_web_app.a_adapters.repository import AbstractRepository
from movie_web_app.a_adapters.memory_repository import MemoryRepository

from movie_web_app.a_blueprints import list_movies

"""
TEST_DATA_PATH = os.path.join('C:', os.sep, 'Users', 'nigel', 'Desktop', 'University Work',
                              'Year 3 (2020)', 'Semester 2', 'CompSci 235', '235 assignments',
                              '235 A3', 'CS235-A3', 'tests', 'data')
"""
TEST_DATA_PATH_MEMORY = os.path.join('C:', os.sep, 'Users', 'nigel', 'Desktop', 'University Work',
                              'Year 3 (2020)', 'Semester 2', 'CompSci 235', '235 assignments',
                              '235 A3', 'CS235-A3', 'tests', 'data', 'memory')
TEST_DATA_PATH_DATABASE = os.path.join('C:', os.sep, 'Users', 'nigel', 'Desktop', 'University Work',
                              'Year 3 (2020)', 'Semester 2', 'CompSci 235', '235 assignments',
                              '235 A3', 'CS235-A3', 'tests', 'data', 'database')

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///movies-test.db'

@pytest.fixture
def repo():
    repo = AbstractRepository()
    return repo

@pytest.fixture
def memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH_MEMORY, repo)
    return repo

@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH_MEMORY, repo)
    return repo

@pytest.fixture
def database_engine():
    database_engine = create_engine(TEST_DATABASE_URI_FILE)
    clear_mappers()
    metadata.create_all(database_engine)  # Conditionally create database tables.
    for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
        database_engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
    database_repository.populate(session_factory, TEST_DATA_PATH_DATABASE)
    database_repository.second_populate(session_factory, TEST_DATA_PATH_DATABASE)
    yield database_engine
    metadata.drop_all(database_engine)
    clear_mappers()

@pytest.fixture
def empty_session():
    database_engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(database_engine)
    for table in reversed(metadata.sorted_tables):
        database_engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
    yield session_factory()
    metadata.drop_all(database_engine)
    clear_mappers()

@pytest.fixture
def session():
    clear_mappers()
    database_engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(database_engine)
    for table in reversed(metadata.sorted_tables):
        database_engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
    database_repository.populate(session_factory, TEST_DATA_PATH_DATABASE)
    database_repository.second_populate(session_factory, TEST_DATA_PATH_DATABASE)
    yield session_factory()
    metadata.drop_all(database_engine)
    clear_mappers()

@pytest.fixture
def session_factory():
    clear_mappers()
    database_engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(database_engine)
    for table in reversed(metadata.sorted_tables):
        database_engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
    database_repository.populate(session_factory, TEST_DATA_PATH_DATABASE)
    database_repository.second_populate(session_factory, TEST_DATA_PATH_DATABASE)
    yield session_factory
    metadata.drop_all(database_engine)
    clear_mappers()


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,                                # Set to True during testing.
        'REPOSITORY': 'database',                         # Set to 'memory' or 'database' depending on desired repository.
        'TEST_DATA_PATH': TEST_DATA_PATH_DATABASE,        # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False                       # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()

class AuthenticationManager:
    def __init__(self, client):
        self._client = client

    def login(self, user_name='asdfgh', password='123Qweasd'):
        return self._client.post(
            'authen/login',
            data={'user_name': user_name, 'password': password}
        )

    def logout(self):
        return self._client.get('/authen/logout')

@pytest.fixture
def authen(client):
    return AuthenticationManager(client)