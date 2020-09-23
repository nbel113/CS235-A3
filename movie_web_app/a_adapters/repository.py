import abc
from movie_web_app.domain.model import Director, Genre, Actor, Movie, Review, User, WatchList

repo_instance = None
class RepositoryException(Exception):
    def __init__(self, message=None):
        pass

class AbstractRepository(abc.ABC):
    #Movies
    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """ Adds a Movie to the repository."""
        raise NotImplementedError
    @abc.abstractmethod
    def get_movie(self, title: str) -> Movie:
        """ Returns the Movie stored in the repository. """
        raise NotImplementedError

    #Authen
    @abc.abstractmethod
    def add_user(self, user: User):
        """ Adds a User to the repository."""
        raise NotImplementedError
    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """ Returns the User stored in the repository. """
        raise NotImplementedError

    #Reviews
    @abc.abstractmethod
    def add_review(self, user: User, review: Review):
        """ Adds a Review to the repository."""
        raise NotImplementedError
    @abc.abstractmethod
    def get_review(self, review: Review):
        """ Returns the Review stored in the repository. """
        raise NotImplementedError