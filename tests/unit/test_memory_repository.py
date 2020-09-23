from datetime import date, datetime
from typing import List

import pytest

from movie_web_app.domain.model import Director, Genre, Actor, Movie, Review, User, WatchList
from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from movie_web_app.activitysimulations.watchingsimulation import MovieWatchingSimulation

from movie_web_app.a_adapters.repository import RepositoryException
import movie_web_app.a_adapters.authen_services as authen_services
from movie_web_app.a_adapters.authen_services import NameNotUniqueException

#movies
def test_repo_can_add_movie(memory_repo):
    movie = Movie("ABC", 1987)
    memory_repo.add_movie(movie)
    assert memory_repo.get_movie("ABC") is movie
    assert movie in memory_repo.get_all_movies()

def test_repo_can_get_movie(memory_repo):
    movie = memory_repo.get_movie("Star Trek")
    assert movie == Movie("Star Trek", 2009)

def test_repo_cannot_get_non_existent_movie(memory_repo):
    movie = memory_repo.get_movie("Stat Trek")
    assert movie is None

def test_repo_can_get_all_movies(memory_repo):
    all_movies = memory_repo.get_all_movies()
    assert len(all_movies) == 1000

#search
    #title
def test_repo_can_get_movies_by_search_title(memory_repo):
    movies = memory_repo.get_movies_by_search_title("Star")
    assert repr(movies) == "[<Movie Star Trek Beyond, 2016>, <Movie Star Wars: Episode VII - The Force Awakens, 2015>, <Movie Star Trek, 2009>, <Movie The Fault in Our Stars, 2014>, <Movie Stardust, 2007>, <Movie Star Trek Into Darkness, 2013>, <Movie Popstar: Never Stop Never Stopping, 2016>]"
    assert len(movies) == 7
def test_repo_can_get_movies_by_search_title_lower(memory_repo):
    movies = memory_repo.get_movies_by_search_title("star")
    assert repr(movies) == "[<Movie Star Trek Beyond, 2016>, <Movie Star Wars: Episode VII - The Force Awakens, 2015>, <Movie Star Trek, 2009>, <Movie The Fault in Our Stars, 2014>, <Movie Stardust, 2007>, <Movie Star Trek Into Darkness, 2013>, <Movie Popstar: Never Stop Never Stopping, 2016>]"
    assert len(movies) == 7
def test_repo_search_with_many_titles(memory_repo):
    movies = memory_repo.get_movies_by_search_title("star, Space")
    assert repr(movies) == "[<Movie Star Trek Beyond, 2016>, <Movie Star Wars: Episode VII - The Force Awakens, 2015>, <Movie Star Trek, 2009>, <Movie The Fault in Our Stars, 2014>, <Movie Stardust, 2007>, <Movie Star Trek Into Darkness, 2013>, <Movie Popstar: Never Stop Never Stopping, 2016>, <Movie Crawlspace, 2016>]"
    assert len(movies) == 8

    #director
def test_repo_can_get_movies_by_search_director(memory_repo):
    movies = memory_repo.get_movies_by_search_director("Tim B")
    assert repr(movies) == "[<Movie Miss Peregrine's Home for Peculiar Children, 2016>, <Movie Alice in Wonderland, 2010>, <Movie Sweeney Todd: The Demon Barber of Fleet Street, 2007>, <Movie Dark Shadows, 2012>]"
    assert len(movies) == 4
def test_repo_can_get_movies_by_search_director_lower(memory_repo):
    movies = memory_repo.get_movies_by_search_director("tim b")
    assert repr(movies) == "[<Movie Miss Peregrine's Home for Peculiar Children, 2016>, <Movie Alice in Wonderland, 2010>, <Movie Sweeney Todd: The Demon Barber of Fleet Street, 2007>, <Movie Dark Shadows, 2012>]"
    assert len(movies) == 4
def test_repo_search_with_many_directors(memory_repo):
    movies = memory_repo.get_movies_by_search_director("Tim Burton, Tim Miller")
    assert repr(movies) == "[<Movie Deadpool, 2016>, <Movie Miss Peregrine's Home for Peculiar Children, 2016>, <Movie Alice in Wonderland, 2010>, <Movie Sweeney Todd: The Demon Barber of Fleet Street, 2007>, <Movie Dark Shadows, 2012>]"
    assert len(movies) == 5

    #actor
def test_repo_can_get_movies_by_search_actor(memory_repo):
    movies = memory_repo.get_movies_by_search_actor("Ryan Reynolds")
    assert repr(movies) == "[<Movie Deadpool, 2016>, <Movie Woman in Gold, 2015>, <Movie X-Men Origins: Wolverine, 2009>, <Movie Criminal, 2016>, <Movie The Proposal, 2009>, <Movie Green Lantern, 2011>, <Movie Self/less, 2015>]"
    assert len(movies) == 7
def test_repo_can_get_movies_by_search_actor_lower(memory_repo):
    movies = memory_repo.get_movies_by_search_actor("ryan reynolds")
    assert repr(
        movies) == "[<Movie Deadpool, 2016>, <Movie Woman in Gold, 2015>, <Movie X-Men Origins: Wolverine, 2009>, <Movie Criminal, 2016>, <Movie The Proposal, 2009>, <Movie Green Lantern, 2011>, <Movie Self/less, 2015>]"
    assert len(movies) == 7
def test_repo_search_with_many_actors(memory_repo):
    movies = memory_repo.get_movies_by_search_actor("Ryan Reynolds, 50 Cent")
    assert repr(
        movies) == "[<Movie Deadpool, 2016>, <Movie Woman in Gold, 2015>, <Movie X-Men Origins: Wolverine, 2009>, <Movie Criminal, 2016>, <Movie The Proposal, 2009>, <Movie Green Lantern, 2011>, <Movie Escape Plan, 2013>, <Movie Self/less, 2015>]"
    assert len(movies) == 8

    #genre
def test_repo_can_get_movies_by_search_genre(memory_repo):
    movies = memory_repo.get_movies_by_search_genre("Horror")
    assert len(movies) == 119
def test_repo_can_get_movies_by_search_genre_lower(memory_repo):
    movies = memory_repo.get_movies_by_search_genre("horror")
    assert len(movies) == 119
def test_repo_search_with_many_genres(memory_repo):
    movies = memory_repo.get_movies_by_search_genre("horror, comedy")
    assert len(movies) == 398

    #multiple search boxes
def test_repo_can_reject_if_input_is_only_blank(memory_repo):
    movies = memory_repo.get_movies_by_search_title("")
    directors = memory_repo.get_movies_by_search_director(" ")
    actors = memory_repo.get_movies_by_search_actor("  ")
    genres = memory_repo.get_movies_by_search_genre("   ")
    assert repr(movies) == "None"
    assert repr(directors) == "None"
    assert repr(actors) == "None"
    assert repr(genres) == "None"
def test_repo_several_fields_1(memory_repo):
    title_search_result = memory_repo.get_movies_by_search_title(" ")
    director_search_result = memory_repo.get_movies_by_search_director("Tim Burton")
    actors_search_result = memory_repo.get_movies_by_search_actor("Johnny Depp")
    genres_search_result = memory_repo.get_movies_by_search_genre("Fantasy")

    args = []  # list for the arguments
    search_results_lists = [
        title_search_result,
        director_search_result,
        actors_search_result,
        genres_search_result
    ]
    for i in range(len(search_results_lists)):
        if search_results_lists[i] is not None:
            args.append(set(search_results_lists[i]))

    intersection_set = set.intersection(*args)  # *args means variable number of positional arguments
    intersection_list = list(intersection_set)
    assert len(intersection_list) == 2
def test_repo_several_fields_2(memory_repo):
    title_search_result = memory_repo.get_movies_by_search_title("a")
    director_search_result = memory_repo.get_movies_by_search_director("b")
    actors_search_result = memory_repo.get_movies_by_search_actor("c")
    genres_search_result = memory_repo.get_movies_by_search_genre("d")

    args = []  # list for the arguments

    search_results_lists = [
        title_search_result,
        director_search_result,
        actors_search_result,
        genres_search_result
    ]

    for i in range(len(search_results_lists)):
        if search_results_lists[i] is not None:
            args.append(set(search_results_lists[i]))

    intersection_set = set.intersection(*args)  # *args means variable number of positional arguments
    intersection_list = list(intersection_set)
    assert len(intersection_list) == 85

#user/authen
def test_repo_can_add_a_user(memory_repo):
    user = User('qwerty', '123Qweasd')
    memory_repo.add_user(user)

    assert memory_repo.get_user('qwerty') is user
    assert user in memory_repo.get_all_users()

def test_repo_can_retrieve_a_user(memory_repo):
    user = User('qwerty', '123Qweasd')
    memory_repo.add_user(user)
    retrieve_user = memory_repo.get_user('qwerty')
    assert retrieve_user == User('qwerty', '123Qweasd')

def test_repo_does_not_retrieve_a_non_existent_user(memory_repo):
    user = memory_repo.get_user('qwe')
    assert user is None

def test_repo_can_retrieve_user_count(memory_repo):
    original_user_count = len(memory_repo.get_all_users())
    user1 = User('qwerty', '123Qweasd')
    user2 = User('qwe', '123Qweasd')
    memory_repo.add_user(user1)
    memory_repo.add_user(user2)
    assert len(memory_repo.get_all_users()) == original_user_count + 2

#reviews
def test_repo_can_add_a_review(memory_repo):
    new_username = "qwerty"
    new_password = "123Qweasd"
    user = User(new_username, new_password)
    memory_repo.add_user(user)

    review_movie_title = "Star Trek"
    review_movie = memory_repo.get_movie(review_movie_title)
    review_text = "Not as good as the original series"
    review_score = 6
    review = Review(review_movie, review_text, review_score)

    memory_repo.add_review(user, review)

    assert review in memory_repo.get_all_reviews()

def test_repo_can_retrieve_a_review(memory_repo):
    new_username = "qwerty"
    new_password = "123Qweasd"
    user = User(new_username, new_password)
    memory_repo.add_user(user)

    review_movie_title_1 = "Star Trek"
    review_movie_1 = memory_repo.get_review(review_movie_title_1)
    review_text_1 = "Not as good as the original series"
    review_score_1 = 6
    review1 = Review(review_movie_1, review_text_1, review_score_1)

    review_movie_title_2 = "Split"
    review_movie_2 = memory_repo.get_review(review_movie_title_2)
    review_text_2 = "Pretty good"
    review_score_2 = 8
    review2 = Review(review_movie_2, review_text_2, review_score_2)

    memory_repo.add_review(user, review1)
    memory_repo.add_review(user, review2)

    retrieve_review = memory_repo.get_review(review1.review_id)
    assert retrieve_review == Review(review_movie_1, review_text_1, review_score_1)

def test_repo_does_not_retrieve_a_non_existent_review(memory_repo):
    review = memory_repo.get_review(',./;') #a review id that would never exist
    assert review is None

def test_repo_can_retrieve_review_count(memory_repo):
    new_username = "qwerty"
    new_password = "123Qweasd"
    user = User(new_username, new_password)
    memory_repo.add_user(user)

    review_movie_title_1 = "Star Trek"
    review_movie_1 = memory_repo.get_review(review_movie_title_1)
    review_text_1 = "Not as good as the original series"
    review_score_1 = 6
    review1 = Review(review_movie_1, review_text_1, review_score_1)

    review_movie_title_2 = "Split"
    review_movie_2 = memory_repo.get_review(review_movie_title_2)
    review_text_2 = "Pretty good"
    review_score_2 = 8
    review2 = Review(review_movie_2, review_text_2, review_score_2)

    memory_repo.add_review(user, review1)
    memory_repo.add_review(user, review2)

    assert len(memory_repo.get_all_reviews()) == 2
