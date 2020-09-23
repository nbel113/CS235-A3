from datetime import date, datetime
from typing import List

import pytest

from movie_web_app.domain.model import Director, Genre, Actor, Movie, Review, TempReview, User, WatchList
from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from movie_web_app.activitysimulations.watchingsimulation import MovieWatchingSimulation

from movie_web_app.a_adapters.repository import RepositoryException
import movie_web_app.a_adapters.authen_services as authen_services
import movie_web_app.a_adapters.review_services as review_services
from movie_web_app.a_adapters.authen_services import NameNotUniqueException, UnknownUserException, AuthenticationException
from movie_web_app.a_adapters.review_services import UnknownUserException

#authen/user
def test_can_add_user(memory_repo):
    original_user_count = len(memory_repo.get_all_users())
    new_username = "qwerty"
    new_password = "123Qweasd"

    authen_services.add_user(new_username, new_password, memory_repo)
    assert len(memory_repo.get_all_users()) == original_user_count + 1
    user_as_dict = authen_services.get_user(new_username, memory_repo)
    assert user_as_dict['user_name'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')

def test_can_add_many_users(memory_repo):
    original_user_count = len(memory_repo.get_all_users())
    new_username = "qwerty"
    new_password = "123Qweasd"
    authen_services.add_user(new_username, new_password, memory_repo)
    authen_services.add_user("qwe", "123Qweasd", memory_repo)
    assert len(memory_repo.get_all_users()) == original_user_count + 2

def test_can_reject_user_with_existing_username(memory_repo):
    original_user_count = len(memory_repo.get_all_users())
    new_username = "qwerty"
    new_password = "123Qweasd"
    try:
        authen_services.add_user(new_username, new_password, memory_repo)
        authen_services.add_user(new_username, new_password, memory_repo)
    except NameNotUniqueException:
        assert len(memory_repo.get_all_users()) == original_user_count + 1
        assert True

def test_can_retrieve_user(memory_repo):
    new_username = "qwerty"
    new_password = "123Qweasd"
    authen_services.add_user(new_username, new_password, memory_repo)
    assert authen_services.get_user("qwerty", memory_repo)['user_name'] == "qwerty"

def test_authentication_with_valid_credentials(memory_repo):
    new_username = "qwerty"
    new_password = "123Qweasd"

    authen_services.add_user(new_username, new_password, memory_repo)
    try:
        authen_services.authenticate_user(new_username, new_password, memory_repo)
    except AuthenticationException:
        assert False

def test_authentication_with_invalid_credentials(memory_repo):
    new_username = "qwerty"
    new_password = "123Qweasd"

    authen_services.add_user(new_username, new_password, memory_repo)
    try:
        authen_services.authenticate_user(new_username, 'qwertyuiop', memory_repo)
    except AuthenticationException:
        assert True

#reviews
def test_can_add_review(memory_repo):
    new_username = "qwerty"
    new_password = "123Qweasd"
    user = User(new_username, new_password)
    memory_repo.add_user(user)

    review_movie_title = "Star Trek"
    review_movie = memory_repo.get_movie(review_movie_title)
    review_text = "Not as good as the original series"
    review_score = 6
    review = Review(review_movie, review_text, review_score)

    review_services.add_review(user, review)
    assert review in user.reviews
def test_cannot_add_review_with_no_user(memory_repo):
    user = None
    memory_repo.add_user(user)

    review_movie_title = "Star Trek"
    review_movie = memory_repo.get_movie(review_movie_title)
    review_text = "Not as good as the original series"
    review_score = 6
    review = Review(review_movie, review_text, review_score)

    try:
        review_services.add_review(user, review)
        assert review in user.reviews
    except UnknownUserException:
        assert True
def test_can_get_reviews_from_user(memory_repo):
    new_username = "qwerty"
    new_password = "123Qweasd"
    user = User(new_username, new_password)
    memory_repo.add_user(user)

    review_movie_title = "Star Trek"
    review_movie = memory_repo.get_movie(review_movie_title)
    review_text = "Not as good as the original series"
    review_score = 6
    review = Review(review_movie, review_text, review_score)
    review_services.add_review(user, review)
    assert review in review_services.get_reviews_from_user(new_username, memory_repo)

def test_can_get_review_by_user_and_id(memory_repo):
    new_username = "qwerty"
    new_password = "123Qweasd"
    user = User(new_username, new_password)
    memory_repo.add_user(user)

    review_movie_title = "Star Trek"
    review_movie = memory_repo.get_movie(review_movie_title)
    review_text = "Not as good as the original series"
    review_score = 6
    review = Review(review_movie, review_text, review_score)

    session_user_name = new_username
    review_id = review.review_id

    # Call the service layer to add the comment.
    review_services.add_review(user, review)
    a = review_services.get_review_by_user_and_id(session_user_name, review_id, memory_repo)

    assert review is a

def test_can_edit_review_change_all(memory_repo):
    new_username = "qwerty"
    new_password = "123Qweasd"
    user = User(new_username, new_password)
    memory_repo.add_user(user)

    review_movie_title = "Star Trek"
    review_movie = memory_repo.get_movie(review_movie_title)
    review_text = "Not as good as the original series"
    review_rating = 6
    review = Review(review_movie, review_text, review_rating)

    new_review_movie_title = "Split"
    new_review_movie = memory_repo.get_movie(new_review_movie_title)
    new_review_text = "Very Good"
    new_review_rating = 8
    new_review = TempReview(new_review_movie, new_review_text, new_review_rating)

    review_services.edit_review(review, new_review)
    assert review.movie == new_review_movie
    assert review.review_text == new_review_text
    assert review.rating == new_review_rating

def test_can_edit_review_change_some(memory_repo):
    new_username = "qwerty"
    new_password = "123Qweasd"
    user = User(new_username, new_password)
    memory_repo.add_user(user)

    review_movie_title = "Star Trek"
    review_movie = memory_repo.get_movie(review_movie_title)
    review_text = "Not as good as the original series"
    review_rating = 6
    review = Review(review_movie, review_text, review_rating)

    new_review_movie_title = ""
    new_review_movie = memory_repo.get_movie(new_review_movie_title)
    new_review_text = "Very Good"
    new_review_rating = 8
    new_review = TempReview(new_review_movie, new_review_text, new_review_rating)

    review_services.edit_review(review, new_review)
    assert review.movie == review_movie
    assert review.review_text == new_review_text
    assert review.rating == new_review_rating
def test_can_edit_review_change_none(memory_repo):
    new_username = "qwerty"
    new_password = "123Qweasd"
    user = User(new_username, new_password)
    memory_repo.add_user(user)

    review_movie_title = "Star Trek"
    review_movie = memory_repo.get_movie(review_movie_title)
    review_text = "Not as good as the original series"
    review_rating = 6
    review = Review(review_movie, review_text, review_rating)

    new_review_movie_title = None
    new_review_movie = memory_repo.get_movie(new_review_movie_title)
    new_review_text = ""
    new_review_rating = None
    new_review = TempReview(new_review_movie, new_review_text, new_review_rating)

    review_services.edit_review(review, new_review)
    assert review.movie == review_movie
    assert review.review_text == review_text
    assert review.rating == review_rating

def test_can_delete_review(memory_repo):
    new_username = "qwerty"
    new_password = "123Qweasd"
    user = User(new_username, new_password)
    memory_repo.add_user(user)

    review_movie_title = "Star Trek"
    review_movie = memory_repo.get_movie(review_movie_title)
    review_text = "Not as good as the original series"
    review_rating = 6
    review = Review(review_movie, review_text, review_rating)

    review_services.add_review(user, review)
    review_services.delete_review(new_username, review, memory_repo)

    assert review not in review_services.get_reviews_from_user(new_username, memory_repo)

