import os

from movie_web_app.a_adapters.repository import AbstractRepository, RepositoryException
from movie_web_app.domain.model import Director, Genre, Actor, Movie, Review, User, WatchList
from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from movie_web_app.datafilereaders.user_file_csv_reader import UserFileCSVReader

class MemoryRepository(AbstractRepository):
    def __init__(self):
        self._movies = list()
        self._users = list()
        self._reviews = list()
#movies
    def add_movie(self, movie: Movie):
        self._movies.append(movie)
    def get_movie(self, title: str) -> Movie:
        return next((movie for movie in self._movies if movie.title == title), None)
    def get_all_movies(self):
        movie_list = list()
        for movie in self._movies:
            movie_list.append(movie)
        return movie_list
#search
    def get_movies_by_search_title(self, title_search: str):
        title_search = title_search.strip().casefold()
        if title_search == '':
            return None
        titles_list = title_search.split(",")
        for i in range(len(titles_list)):
            titles_list[i] = titles_list[i].strip()
        #print(titles_list)
        results = []
        for movie in self._movies:
            for i in range(len(titles_list)):
                if movie.title.casefold().find(titles_list[i]) is not -1: #if the text is a substring
                    results.append(movie)
        return results
    def get_movies_by_search_director(self, director_search: str):
        director_search = director_search.strip().casefold()
        if director_search == '':
            return None
        directors_list = director_search.split(",")
        for i in range(len(directors_list)):
            directors_list[i] = directors_list[i].strip()
        #print(directors_list)
        results = []
        for movie in self._movies:
            for i in range(len(directors_list)):
                if movie.director.casefold().find(directors_list[i]) is not -1:  # if the text is a substring
                    results.append(movie)
        return results
    def get_movies_by_search_actor(self, actor_search: str):
        actor_search = actor_search.strip().casefold()
        if actor_search == '':
            return None
        actors_list = actor_search.split(",")
        for i in range(len(actors_list)):
            actors_list[i] = actors_list[i].strip()
        #print(actors_list)
        results = []
        for movie in self._movies:
            for i in range(len(actors_list)):
                if repr(movie.actors).casefold().find(actors_list[i]) is not -1:  # if the text is a substring
                    results.append(movie)
        return results
    def get_movies_by_search_genre(self, genre_search: str):
        genre_search = genre_search.strip().casefold()
        if genre_search == '':
            return None
        genres_list = genre_search.split(",")
        for i in range(len(genres_list)):
            genres_list[i] = genres_list[i].strip()
        #print(genres_list)
        results = []
        for movie in self._movies:
            for i in range(len(genres_list)):
                if repr(movie.genres).casefold().find(genres_list[i]) is not -1:  # if the text is a substring
                    results.append(movie)
        return results
#user/authen
    def add_user(self, user: User):
        self._users.append(user)
    def get_user(self, user_name: str) -> User:
        return next((user for user in self._users if user.user_name == user_name), None)
    def get_all_users(self):
        users_list = list()
        for user in self._users:
            users_list.append(user)
        return users_list
#reviews
    def add_review(self, user: User, review: Review):
        self._reviews.append(review)
    def get_review(self, review_id: str):
        return next((review for review in self._reviews if review.review_id == review_id), None)
    def get_all_reviews(self):
        reviews_list = list()
        for review in self._reviews:
            reviews_list.append(review)
        return reviews_list

def load_movies(data_path: str, repo: MemoryRepository):
    movie_file_reader = MovieFileCSVReader(os.path.join(data_path, 'Data1000Movies.csv'))
    movie_file_reader.read_csv_file()
    for movie in movie_file_reader.dataset_of_movies:
        repo.add_movie(movie)

def load_users(data_path: str, repo: MemoryRepository):
    user_file_reader = UserFileCSVReader(os.path.join(data_path, 'users.csv'))
    user_file_reader.read_csv_file()
    for user in user_file_reader.dataset_of_users:
        repo.add_user(user)

def populate(data_path: str, repo: MemoryRepository):
    # Load movies into the repository.
    load_movies(data_path, repo)
    load_users(data_path, repo)