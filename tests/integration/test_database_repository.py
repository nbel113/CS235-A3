from datetime import date, datetime

import pytest

from movie_web_app.a_adapters.database_repository import SqlAlchemyRepository
from movie_web_app.domain.model import *
from movie_web_app.a_adapters.repository import *

def test_repository_can_retrieve_movie_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    all_movies = repo.get_all_movies()

    # Check that the query returned 1000 Movies.
    assert len(all_movies) == 1000
    
def test_repository_can_add_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_movies = len(repo.get_all_movies())

    new_movie_id = number_of_movies + 1

    movie = Movie(
        "qweasd",
        2020,
    )
    movie.director = Director("Taika Waititi")
    movie.description = "This is a movie 2"
    movie.runtime_minutes = 123
    repo.add_movie(movie)

    assert repo.get_movie(movie.title) == movie

def test_repository_can_retrieve_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie("Fury")
    assert movie == Movie("Fury", 2014)
    
def test_repository_does_not_retrieve_a_non_existent_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie("abc")
    assert movie is None

def test_repository_can_retrieve_movie_director_full_name(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie("Star Trek")
    assert repo.get_movie_director_full_name(movie.directorID) == "J.J. Abrams"

def test_repository_can_retrieve_movie_actors(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie("Star Trek")
    assert len(repo.get_movie_actors(movie.movieID)) == 4

def test_repository_can_retrieve_movie_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie("Star Trek")
    assert len(repo.get_movie_genres(movie.movieID)) == 3

def test_repository_can_retrieve_movies_by_search_title(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert len(repo.get_movies_by_search_title("Star")) == 7
def test_repository_can_retrieve_movies_by_several_search_titles(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert len(repo.get_movies_by_search_title("Star, space")) == 8
    
def test_repository_can_retrieve_movies_by_search_director(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert len(repo.get_movies_by_search_director("J.J.")) == 5
def test_repository_can_retrieve_movies_by_several_search_directors(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert len(repo.get_movies_by_search_director("J.J., Taika")) == 6
    
def test_repository_can_retrieve_movies_by_search_actor(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert len(repo.get_movies_by_search_actor("a")) == 3178
def test_repository_can_retrieve_movies_by_several_search_actor(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert len(repo.get_movies_by_search_actor("a, b")) == 4089

def test_repository_can_retrieve_movies_by_search_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert len(repo.get_movies_by_search_genre("Horror")) == 119
def test_repository_can_retrieve_movies_by_several_search_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert len(repo.get_movies_by_search_genre("Horror, Comedy")) == 398

def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('dave')
    print(user2, user)
    assert user2 == user and user2 is user

def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('asdfgh')
    assert user == User('asdfgh', '123Qweasd')

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('xXx~qwerty~xXx')
    assert user is None

def test_repository_can_retrieve_user_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    all_users = repo.get_all_users()

    # Check that the query returned 1000 Movies.
    assert len(all_users) == 2

def test_repository_can_add_and_get_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('asdfgh')
    movie = repo.get_movie("Moana")
    review_text = "This movie was very enjoyable."
    rating = 8
    review = Review(movie, review_text, rating)
    repo.add_review(user, review)

    assert repo.get_review_by_user_and_id(user.user_name, review.reviewID, repo) is review

def test_repository_can_retrieve_reviews_from_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user1 = repo.get_user('asdfgh')
    user2 = repo.get_user('zxcvbn')
    movie1 = repo.get_movie("Fury")
    movie2 = repo.get_movie("Star Trek")

    review_text = "This movie was very enjoyable."
    rating = 8

    review1 = Review(movie1, review_text, rating)
    review2 = Review(movie2, review_text, rating)
    review3 = Review(movie1, review_text, rating)
    review4 = Review(movie2, review_text, rating)
    review5 = Review(movie2, "meh", rating)

    repo.add_review(user1, review1)
    repo.add_review(user1, review2)
    repo.add_review(user2, review3)
    repo.add_review(user2, review4)
    repo.add_review(user2, review5)

    assert len(repo.get_reviews_from_user("asdfgh", repo)) == 2
    assert len(repo.get_reviews_from_user("zxcvbn", repo)) == 3


def test_repository_can_retrieve_review_by_user_and_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user1 = repo.get_user('asdfgh')
    user2 = repo.get_user('zxcvbn')
    movie1 = repo.get_movie("Fury")
    movie2 = repo.get_movie("Star Trek")

    review_text = "This movie was very enjoyable."
    rating = 8

    review1 = Review(movie1, review_text, rating)
    review2 = Review(movie2, review_text, rating)
    review3 = Review(movie1, review_text, rating)
    review4 = Review(movie2, review_text, rating)
    review5 = Review(movie2, "meh", rating)

    repo.add_review(user1, review1)
    repo.add_review(user1, review2)
    repo.add_review(user2, review3)
    repo.add_review(user2, review4)
    repo.add_review(user2, review5)

    assert repo.get_review_by_user_and_id("asdfgh", 2, repo) == review2

def test_repository_can_edit_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie1 = repo.get_movie("Fury")
    movie2 = repo.get_movie("Star Trek")

    review_text = "This movie was very enjoyable."
    rating = 8

    review1 = Review(movie1, review_text, rating)
    review2 = Review(movie1, review_text, rating)
    review3 = Review(movie1, review_text, rating)
    review4 = Review(movie1, review_text, rating)

    new_review1 = Review(movie2, review_text, rating)
    new_review2 = Review(movie1, "Very Very Good", rating)
    new_review3 = Review(movie1, review_text, 10)
    new_review4 = Review(movie2, "Very Very Good", 10)

    repo.edit_review(review1, new_review1)
    assert review1.movie == movie2

    repo.edit_review(review2, new_review2)
    assert review2.review_text == "Very Very Good"

    repo.edit_review(review3, new_review3)
    assert review3.rating == 10

    repo.edit_review(review4, new_review4)
    assert review4.movie == movie2 and review4.review_text == "Very Very Good" and review4.rating == 10

def test_repository_can_delete_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user1 = repo.get_user('asdfgh')

    movie1 = repo.get_movie("Fury")
    movie2 = repo.get_movie("Star Trek")

    review_text = "This movie was very enjoyable."
    rating = 8

    review1 = Review(movie1, review_text, rating)
    review2 = Review(movie2, review_text, rating)

    repo.add_review(user1, review1)
    repo.add_review(user1, review2)
    assert len(user1.reviews) == 2
    repo.delete_review(user1.user_name, review1, repo)
    assert len(user1.reviews) == 1
