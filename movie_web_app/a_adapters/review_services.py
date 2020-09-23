from typing import List, Iterable

from movie_web_app.a_adapters.repository import AbstractRepository

from movie_web_app.domain.model import Director, Genre, Actor, Movie, Review, TempReview, User, WatchList

class UnknownUserException(Exception):
    pass

def add_review(user: User, review: Review):
    if user is None:
        raise UnknownUserException
    if (review not in user.reviews):
        user.add_review(review)

def get_reviews_from_user(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    return user.reviews

def get_review_by_user_and_id(session_user_name: str, review_id, repo: AbstractRepository):
    user = repo.get_user(session_user_name)
    """
    print(user.reviews)
    print("target id:", review_id)
    for review in user.reviews:
        print("\treview id:", review.review_id)
    """
    return next((review for review in user.reviews if str(review.review_id) == str(review_id)), None)

def edit_review(review: Review, new_review: TempReview):
    edit_occurred = False
    """
    if new_review.movie is None or new_review.movie.title == "":
        print("A1a")
    else:
        print("A2")
        review.movie = new_review.movie
        edit_occurred = True

    if new_review.review_text == "" or new_review.review_text is None:
        print("B1")
    else:
        print("B2")
        review.review_text = new_review.review_text
        edit_occurred = True

    if new_review.rating == "" or new_review.rating is None:
        print("C1")
    else:
        print("C2")
        review.rating = new_review.rating
        edit_occurred = True
    """

    if not (new_review.movie is None or new_review.movie.title == ""):
        review.movie = new_review.movie
        edit_occurred = True

    if not (new_review.review_text == "" or new_review.review_text is None):
        review.review_text = new_review.review_text
        edit_occurred = True

    if not (new_review.rating == "" or new_review.rating is None):
        review.rating = new_review.rating
        edit_occurred = True

    if edit_occurred:
        review.latest_edit = new_review.timestamp


def delete_review(session_user_name: str, review: Review, repo: AbstractRepository):
    user = repo.get_user(session_user_name)
    return user.reviews.remove(review)
