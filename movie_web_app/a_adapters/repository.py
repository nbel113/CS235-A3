import abc
from typing import List
from datetime import date, datetime

from movie_web_app.domain.model import Director, Genre, Actor, Movie, Review, User, WatchList
from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from movie_web_app.activitysimulations.watchingsimulation import MovieWatchingSimulation


repo_instance = None
class RepositoryException(Exception):
    def __init__(self, message=None):
        pass

class AbstractRepository(abc.ABC):

    #Movies
    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, title: str) -> Movie:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_movies(self):
        raise NotImplementedError

    #Search
    """

    def get_title(self, id: int):
        return next((person for person in self._people if person.id_number == id), None)
    """

    #Authen
    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError
    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        raise NotImplementedError

    #Reviews
    @abc.abstractmethod
    def add_review(self, user: User, review: Review):
        """ Adds a Review to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the Comments stored in the repository. """
        raise NotImplementedError