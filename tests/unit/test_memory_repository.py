from datetime import date, datetime
from typing import List

import pytest

from movie_web_app.domain.model import Director, Genre, Actor, Movie, Review, User, WatchList
from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from movie_web_app.activitysimulations.watchingsimulation import MovieWatchingSimulation

from movie_web_app.a_adapters.repository import RepositoryException

#movies
def test_repo_can_add_movie(movies_repo):
    movie = Movie("ABC", 1987)
    movies_repo.add_movie(movie)
    assert movies_repo.get_movie("ABC") is movie

def test_repo_can_get_movie(movies_repo):
    movie = movies_repo.get_movie("Star Trek")
    assert movie == Movie("Star Trek", 2009)

def test_repo_cannot_get_non_existent_movie(movies_repo):
    movie = movies_repo.get_movie("Stat Trek")
    assert movie is None

def test_repo_can_get_all_movies(movies_repo):
    all_movies = movies_repo.get_all_movies()
    assert len(all_movies) == 1000

#search
    #title
def test_repo_can_get_movies_by_search_title(movies_repo):
    movies = movies_repo.get_movies_by_search_title("Star")
    assert repr(movies) == "[<Movie Star Trek Beyond, 2016>, <Movie Star Wars: Episode VII - The Force Awakens, 2015>, <Movie Star Trek, 2009>, <Movie The Fault in Our Stars, 2014>, <Movie Stardust, 2007>, <Movie Star Trek Into Darkness, 2013>, <Movie Popstar: Never Stop Never Stopping, 2016>]"
    assert len(movies) == 7
def test_repo_can_get_movies_by_search_title_lower(movies_repo):
    movies = movies_repo.get_movies_by_search_title("star")
    assert repr(movies) == "[<Movie Star Trek Beyond, 2016>, <Movie Star Wars: Episode VII - The Force Awakens, 2015>, <Movie Star Trek, 2009>, <Movie The Fault in Our Stars, 2014>, <Movie Stardust, 2007>, <Movie Star Trek Into Darkness, 2013>, <Movie Popstar: Never Stop Never Stopping, 2016>]"
    assert len(movies) == 7
def test_repo_search_with_many_titles(movies_repo):
    movies = movies_repo.get_movies_by_search_title("star, Space")
    assert repr(movies) == "[<Movie Star Trek Beyond, 2016>, <Movie Star Wars: Episode VII - The Force Awakens, 2015>, <Movie Star Trek, 2009>, <Movie The Fault in Our Stars, 2014>, <Movie Stardust, 2007>, <Movie Star Trek Into Darkness, 2013>, <Movie Popstar: Never Stop Never Stopping, 2016>, <Movie Crawlspace, 2016>]"
    assert len(movies) == 8

    #director
def test_repo_can_get_movies_by_search_director(movies_repo):
    movies = movies_repo.get_movies_by_search_director("Tim B")
    assert repr(movies) == "[<Movie Miss Peregrine's Home for Peculiar Children, 2016>, <Movie Alice in Wonderland, 2010>, <Movie Sweeney Todd: The Demon Barber of Fleet Street, 2007>, <Movie Dark Shadows, 2012>]"
    assert len(movies) == 4
def test_repo_can_get_movies_by_search_director_lower(movies_repo):
    movies = movies_repo.get_movies_by_search_director("tim b")
    assert repr(movies) == "[<Movie Miss Peregrine's Home for Peculiar Children, 2016>, <Movie Alice in Wonderland, 2010>, <Movie Sweeney Todd: The Demon Barber of Fleet Street, 2007>, <Movie Dark Shadows, 2012>]"
    assert len(movies) == 4
def test_repo_search_with_many_directors(movies_repo):
    movies = movies_repo.get_movies_by_search_director("Tim Burton, Tim Miller")
    assert repr(movies) == "[<Movie Deadpool, 2016>, <Movie Miss Peregrine's Home for Peculiar Children, 2016>, <Movie Alice in Wonderland, 2010>, <Movie Sweeney Todd: The Demon Barber of Fleet Street, 2007>, <Movie Dark Shadows, 2012>]"
    assert len(movies) == 5

    #actor
def test_repo_can_get_movies_by_search_actor(movies_repo):
    movies = movies_repo.get_movies_by_search_actor("Ryan Reynolds")
    assert repr(movies) == "[<Movie Deadpool, 2016>, <Movie Woman in Gold, 2015>, <Movie X-Men Origins: Wolverine, 2009>, <Movie Criminal, 2016>, <Movie The Proposal, 2009>, <Movie Green Lantern, 2011>, <Movie Self/less, 2015>]"
    assert len(movies) == 7
def test_repo_can_get_movies_by_search_actor_lower(movies_repo):
    movies = movies_repo.get_movies_by_search_actor("ryan reynolds")
    assert repr(
        movies) == "[<Movie Deadpool, 2016>, <Movie Woman in Gold, 2015>, <Movie X-Men Origins: Wolverine, 2009>, <Movie Criminal, 2016>, <Movie The Proposal, 2009>, <Movie Green Lantern, 2011>, <Movie Self/less, 2015>]"
    assert len(movies) == 7
def test_repo_get_movies_by_search_actor(movies_repo):
    movies = movies_repo.get_movies_by_search_actor("Ryan Reynolds, 50 Cent")
    assert repr(
        movies) == "[<Movie Deadpool, 2016>, <Movie Woman in Gold, 2015>, <Movie X-Men Origins: Wolverine, 2009>, <Movie Criminal, 2016>, <Movie The Proposal, 2009>, <Movie Green Lantern, 2011>, <Movie Escape Plan, 2013>, <Movie Self/less, 2015>]"
    assert len(movies) == 8

    #genre
def test_repo_can_get_movies_by_search_genre(movies_repo):
    movies = movies_repo.get_movies_by_search_genre("Horror")
    assert len(movies) == 119
def test_repo_can_get_movies_by_search_genre_lower(movies_repo):
    movies = movies_repo.get_movies_by_search_genre("horror")
    assert len(movies) == 119
def test_repo_get_movies_by_search_genre(movies_repo):
    movies = movies_repo.get_movies_by_search_genre("horror, comedy")
    assert len(movies) == 398

    #multiple search boxes
def test_repo_can_reject_if_input_is_only_whitespace(movies_repo):
    movies = movies_repo.get_movies_by_search_title(" ")
    assert repr(movies) == "None"
    #no length since it's None