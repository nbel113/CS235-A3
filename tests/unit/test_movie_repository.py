from datetime import date, datetime
from typing import List

import pytest

from movie_web_app.domain.model import Director, Genre, Actor, Movie, Review, User, WatchList
from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from movie_web_app.activitysimulations.watchingsimulation import MovieWatchingSimulation

from movie_web_app.a_adapters.repository import RepositoryException

def test_repo_can_add_movie(movies_repo):
    movie = Movie("ABC", 1987)
    movies_repo.add_movie(movie)
    assert movies_repo.get_movie("ABC") is movie

def test_repo_can_get_movie(movies_repo):
    movie = movies_repo.get_movie("Star Trek")
    assert movie == Movie("Star Trek", 2009)

def test_repository_cannot_get_non_existent_movie(movies_repo):
    movie = movies_repo.get_movie("Stat Trek")
    assert movie is None

def test_repository_can_get_movie_count(movies_repo):
    num_of_movies = movies_repo.get_number_of_movies()
    assert num_of_movies == 1000