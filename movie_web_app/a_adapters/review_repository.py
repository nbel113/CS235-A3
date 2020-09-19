from typing import List, Iterable

from movie_web_app.a_adapters.repository import AbstractRepository
from movie_web_app.domain.model import Director, Genre, Actor, Movie, Review, User, WatchList
from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from movie_web_app.activitysimulations.watchingsimulation import MovieWatchingSimulation

class NonExistentReviewException(Exception):
    pass

class UnknownUserException(Exception):
    pass


def add_review(user: User, review: Review, repo: AbstractRepository):
    if user is None:
        raise UnknownUserException
    if (review not in user.reviews):
        user.add_review(review)

def get_reviews_from_user(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    return user.reviews

"""
def review_to_dict(review: Review):
    review_dict = {
        'user_name': review.user.username,
        'review_text': review.review_text
    }
    return review_dict

def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]

"""