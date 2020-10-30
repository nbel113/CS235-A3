import pytest
import datetime
from sqlalchemy.exc import IntegrityError
from movie_web_app.domain.model import *

movie_date = datetime.now()

def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0].lower()
        new_password = values[1]

    empty_session.execute('INSERT INTO user (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT userID from user where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO user (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0].lower(), 'password': value[1]})
    rows = list(empty_session.execute('SELECT userID from user'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_movie(empty_session, movie=None):
    if movie is not None:
        empty_session.execute(
            'INSERT INTO movie (directorID, title, release_year, description, runtime_minutes) VALUES '
            '(:directorID, :title, :release_year, :description, :runtime_minutes)',
            {'directorID': movie.directorID, 'title': movie.title, 'release_year': movie.release_year,
             'description': movie.description, 'runtime_minutes': movie.runtime_minutes}
        )
    else:
        empty_session.execute(
            'INSERT INTO movie (directorID, title, release_year, description, runtime_minutes) VALUES '
            '(:directorID, "ABC123", 2020, "It is a movie", 123)',
            {'directorID': 1}
        )
    row = empty_session.execute('SELECT movieID from movie').fetchone()
    return row[0]

def insert_review(empty_session):
    empty_session.execute(
        'INSERT INTO review (movieID, review_text, rating, timestamp) VALUES \
        (:movieID1, "Was a good movie", :rating1, :date1)',
        {'movieID1': 2, 'rating1': 9, 'date1': datetime.now()}
    )
    row = empty_session.execute('SELECT reviewID from review').fetchone()
    return row[0]

def insert_reviews(empty_session):
    empty_session.execute(
        'INSERT INTO review (movieID, review_text, rating, timestamp) VALUES \
        (:movieID1, "Was a good movie", :rating1, :date1), \
        (:movieID2, "Was an okay movie", :rating2, :date2)',
        {'movieID1': 2, 'rating1': 9, 'date1': datetime.now(),
         'movieID2': 6, 'rating2': 6, 'date2': datetime.now()}
    )

    rows = list(empty_session.execute('SELECT reviewID from review'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_user_review_association(empty_session, user_key, review_keys):
    stmt = 'INSERT INTO user_review (reviewID, userID) VALUES (:reviewID, :userID)'
    for review_key in review_keys:
        empty_session.execute(stmt, {'reviewID': review_key, 'userID': user_key})

def insert_custom_movie_review(empty_session):
    movie_key = insert_movie(empty_session)
    user_key = insert_user(empty_session)

    timestamp_1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    empty_session.execute(
        'INSERT INTO review (movieID, review_text, rating, timestamp) VALUES '
        '(:movieID, "Review 1", 4, :timestamp_1),'
        '(:movieID, "Review 2", 5, :timestamp_2)',
        {'movieID': movie_key, 'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2}
    )
    empty_session.execute(
        'INSERT INTO user_review (reviewID, userID) VALUES '
        '(1, 1),'
        '(2, 1)'
    )

    row = empty_session.execute('SELECT reviewID from review').fetchone()
    return row[0]

def make_movie():
    movie = Movie("ABC123", 2020)
    movie.directorID = 123
    movie.description = "ASDF Movie"
    movie.runtime_minutes = 120
    return movie

def make_user():
    user = User("Andrew", "111")
    return user

def make_review(movie: Movie, review_text: str, rating, user: User, timestamp: datetime = datetime.today()):
    review = Review(movie, review_text, rating)
    review.timestamp = timestamp
    user.add_review(review)

    return review

def test_loading_of_users(empty_session):
    users = list()
    users.append(("Andrew", "1234"))
    users.append(("Cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User("Andrew", "1234"),
        User("Cindy", "999")
    ]

    assert empty_session.query(User).all() == expected

def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM user'))
    assert rows == [("andrew", "111")]

def test_saving_of_users_with_common_username(empty_session):
    insert_user(empty_session, ("Andrew", "1234"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("Andrew", "111")
        empty_session.add(user)
        empty_session.commit()

def test_loading_of_a_movie(empty_session):
    movie_key = insert_movie(empty_session)
    expected_movie = make_movie()
    fetched_movie = empty_session.query(Movie).one()

    assert expected_movie == fetched_movie
    assert movie_key == fetched_movie.movieID

def test_loading_of_a_users_review(empty_session):
    user_key = insert_user(empty_session)
    review_keys = insert_reviews(empty_session)
    print(review_keys)
    insert_user_review_association(empty_session, user_key, review_keys)

    user = empty_session.query(User).get(user_key)
    reviews = [empty_session.query(Review).get(key) for key in review_keys]

    for review in reviews:
        assert review in user.reviews

def test_saving_of_review(empty_session):
    movie_key = insert_movie(empty_session)
    user_key = insert_user(empty_session, ("Andrew", "1234"))

    rows = empty_session.query(Movie).all()
    movie = rows[0]

    rows2 = empty_session.query(User).all()

    for i in range(len(rows2)):
        if rows2[i].user_name == 'andrew':
            user = rows2[i]

    # Create a new Review that is linked with the User.
    review_text = "*clap* meme *clap* review"
    rating = 6
    review = make_review(movie, review_text, rating, user)

    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT reviewID, movieID, review_text, rating FROM review'))
    assert rows == [(review.reviewID, movie_key, review_text, rating)]


def test_saving_of_movie(empty_session):
    movie = make_movie()

    empty_session.add(movie)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT * FROM movie'))
    print(rows)


    assert rows == [(1, 123, 'ABC123', 2020, "ASDF Movie", 120)]


def test_saving_movie_with_review(empty_session):
    movie = make_movie()
    user_key = insert_user(empty_session)
    review_key = [insert_review(empty_session)]

    insert_user_review_association(empty_session, user_key, review_key)

    # Persist the Article (and Tag).
    # Note: it doesn't matter whether we add the Tag or the Article. They are connected
    # bidirectionally, so persisting either one will persist the other.
    empty_session.add(movie)
    empty_session.commit()

    # Test test_saving_of_article() checks for insertion into the articles table.
    rows = list(empty_session.execute('SELECT movieID FROM movie'))
    movie_key = rows[0][0]

    # Check that the review table has a new record.
    rows = list(empty_session.execute('SELECT reviewID, movieID, review_text, rating FROM review'))
    print(rows)
    review_key = rows[0][0]
    assert rows[0] == (1, 2, 'Was a good movie', 9)

    # Check that the user_review table has a new record.
    rows = list(empty_session.execute('SELECT reviewID, userID from user_review'))
    print(rows)

    review_foreign_key = rows[0][0]
    user_foreign_key = rows[0][1]

    assert review_key == review_foreign_key
    assert user_key == user_foreign_key


def test_save_commented_movie(empty_session):
    # Create Movie User objects.
    movie = make_movie()
    user = make_user()

    # Create a new Comment that is bidirectionally linked with the User and Article.
    # Create a new Review that is linked with the User.
    review_text = "*clap* meme *clap* review"
    rating = 6
    review = make_review(movie, review_text, rating, user)

        # Save the new Movie.
    empty_session.add(movie)
    empty_session.commit()

    # Test test_saving_of_article() checks for insertion into the movies table.
    rows = list(empty_session.execute('SELECT movieID FROM movie'))
    movie_key = rows[0][0]

    # Test test_saving_of_users() checks for insertion into the users table.
    rows = list(empty_session.execute('SELECT userID FROM user'))
    user_key = rows[0][0]

    # Check that the comments table has a new record that links to the articles and users
    # tables.
    rows = list(empty_session.execute('SELECT reviewID, movieID, review_text, rating FROM review'))
    assert rows == [(review.reviewID, movie_key, review_text, rating)]
