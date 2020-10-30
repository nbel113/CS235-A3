from sqlalchemy import select, inspect
from movie_web_app.a_adapters.orm import metadata
import datetime


def test_database_populate_inspect_table_names(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['actor', 'director', 'genre', 'movie', 'movie_actor', 'movie_genre', 'review', 'user', 'user_review']

def test_database_populate_select_all_actors_and_movie_actors(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_actors_table = inspector.get_table_names()[0]
    name_of_movie_actors_table = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        # query for records in table tags
        select_statement1 = select([metadata.tables[name_of_actors_table]])
        select_statement2 = select([metadata.tables[name_of_movie_actors_table]])
        result1 = connection.execute(select_statement1)
        result2 = connection.execute(select_statement2)

        all_actors_names = []
        all_movie_actors = []
        for row in result1:
            all_actors_names.append(row['actor_full_name'])
        for row in result2:
            all_movie_actors.append(row['movie_actorID'])

        assert len(all_actors_names) == 1985
        assert len(all_movie_actors) == 3999

def test_database_populate_select_all_directors(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_directors_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table tags
        select_statement = select([metadata.tables[name_of_directors_table]])
        result = connection.execute(select_statement)

        all_director_names = []
        for row in result:
            all_director_names.append(row['director_full_name'])

        assert len(all_director_names) == 644

def test_database_populate_select_all_genres(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[2]
    name_of_movie_genres_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table tags
        select_statement1 = select([metadata.tables[name_of_genres_table]])
        select_statement2 = select([metadata.tables[name_of_movie_genres_table]])
        result1 = connection.execute(select_statement1)
        result2 = connection.execute(select_statement2)

        all_genre_names = []
        all_movie_genres = []
        for row in result1:
            all_genre_names.append(row['genre_name'])
        for row in result2:
            all_movie_genres.append(row['movie_genreID'])

        assert len(all_genre_names) == 20
        assert len(all_movie_genres) == 2555

def test_database_populate_select_all_movies(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_movies_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table tags
        select_statement = select([metadata.tables[name_of_movies_table]])
        result = connection.execute(select_statement)

        all_movie_names = []
        for row in result:
            all_movie_names.append(row['title'])

        assert len(all_movie_names) == 1000


def test_database_populate_select_all_users(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[7]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])

        assert all_users == ['asdfgh', 'zxcvbn']

def test_database_populate_with_reviews(database_engine, session):
    # Get table information
    inspector = inspect(database_engine)
    name_of_reviews_table = inspector.get_table_names()[6]

    with database_engine.connect() as connection:
        # query for records in table review
        select_statement = select([metadata.tables[name_of_reviews_table]])
        result = connection.execute(select_statement)

        all_reviews = []
        for row in result:
            all_reviews.append(row)

        assert len(all_reviews) == 0
