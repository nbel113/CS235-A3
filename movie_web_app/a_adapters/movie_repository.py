import csv
import os
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left
from werkzeug.security import generate_password_hash

from movie_web_app.a_adapters.repository import AbstractRepository, RepositoryException

from movie_web_app.domain.model import Director, Genre, Actor, Movie, Review, User, WatchList
from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from movie_web_app.activitysimulations.watchingsimulation import MovieWatchingSimulation

class MoviesRepository(AbstractRepository):
    def __init__(self):
        self._movies = list()

    def add_movie(self, movie: Movie):
        self._movies.append(movie)

    def get_movie(self, title: str) -> Movie:
        return next((movie for movie in self._movies if movie.title == title), None)

    def get_movies(self):
        movie_list = list()
        for movie in self._movies:
            movie_list.append(movie)
        return movie_list

    def get_number_of_movies(self):
        return len(self.get_movies())

def load_movies(data_path: str, repo: MoviesRepository):
    movie_file_reader = MovieFileCSVReader(os.path.join(data_path, 'Data1000Movies.csv'))
    movie_file_reader.read_csv_file()
    for movie in movie_file_reader.dataset_of_movies:
        repo.add_movie(movie)

def populate(data_path: str, repo: MoviesRepository):
    # Load movies into the repository.
    load_movies(data_path, repo)