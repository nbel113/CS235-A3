import pytest
from flask import session

from movie_web_app.domain.model import Director, Genre, Actor, Movie, Review, User, WatchList
from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from movie_web_app.activitysimulations.watchingsimulation import MovieWatchingSimulation

#Director
def test_director_init():
    director1 = Director("Taika Waititi")
    assert repr(director1) == "<Director Taika Waititi>"
    assert director1.director_full_name is "Taika Waititi"
    director2 = Director("")
    assert director2.director_full_name is None
    director3 = Director(42)
    assert director3.director_full_name is None

def test_director_eq():
    director1 = Director("Taika Waititi")
    director2 = Director("Taika Waititi")
    director3 = Director("Peter Jackson")

    assert (director1 == director2) is True
    assert (director2 == director3) is False

def test_director_lt():
    director1 = Director("Taika Waititi")
    director2 = Director("Taika Waititi")
    director3 = Director("Peter Jackson")

    assert (director1 < director2) is False
    assert (director2 < director3) is False
    assert (director3 < director2) is True

def test_director_hash():
    director1 = Director("Taika Waititi")
    director2 = Director("Peter Jackson")
    director_set = set()

    director_set.add(director1)
    director_set.add(director2)

#Genre
def test_genre_init():
    genre1 = Genre("Horror")
    assert genre1.genre_name is "Horror"
    assert repr(genre1) == "<Genre Horror>"
    genre2 = Genre("")
    assert genre2.genre_name is None
    genre3 = Genre(42)
    assert genre3.genre_name is None

#Actor
def test_actor_init():
    actor1 = Actor("Angelina Jolie")
    assert actor1.actor_full_name is "Angelina Jolie"
    assert repr(actor1) == "<Actor Angelina Jolie>"
    actor2 = Actor("")
    assert actor2.actor_full_name is None
    actor3 = Actor(42)
    assert actor3.actor_full_name is None

def test_actor_add_and_check_colleague():
    actor1 = Actor("Angelina Jolie")
    actor2 = Actor("Jack Black")
    actor1.add_actor_colleague(actor2)
    assert actor1.check_if_this_actor_worked_with(actor2) is True

#Movie
def test_movie_init_basic():
    movie = Movie("Moana", 2016)
    assert repr(movie) == "<Movie Moana, 2016>"
def test_movie_fail_no_name():
    movie = Movie("", 2016)
    assert repr(movie) == "<Movie None, None>"
def test_movie_fail_too_old():
    movie = Movie("Moana", 1886)
    assert repr(movie) == "<Movie None, None>"
def test_movie_no_description():
    movie = Movie("Moana", 2016)
    assert movie.description == ""
def test_movie_set_description():
    movie = Movie("Moana", 2016)
    movie.description = "   This is a movie   "
    assert movie.description == "This is a movie"
def test_movie_set_director():
    movie = Movie("Moana", 2016)
    movie.description = "   This is a movie   "
    assert movie.description == "This is a movie"
    movie.director = Director("Ron Clements")
    assert movie.director.director_full_name is "Ron Clements"
    assert repr(movie.director) == "<Director Ron Clements>"
def test_movie_set_actors():
    movie = Movie("Moana", 2016)
    movie.description = "   This is a movie   "
    assert movie.description == "This is a movie"
    movie.director = Director("Ron Clements")
    assert movie.director.director_full_name is "Ron Clements"
    assert repr(movie.director) == "<Director Ron Clements>"
    actors = [Actor("Auli'i Cravalho"), Actor("Dwayne Johnson"), Actor("Rachel House"), Actor("Temuera Morrison")]
    for actor in actors:
        movie.add_actor(actor)
    assert repr(movie.actors) == "[<Actor Auli\'i Cravalho>, <Actor Dwayne Johnson>, <Actor Rachel House>, <Actor Temuera Morrison>]"
def test_movie_set_genres():
    movie = Movie("Moana", 2016)
    movie.description = "   This is a movie   "
    assert movie.description == "This is a movie"
    movie.director = Director("Ron Clements")
    assert movie.director.director_full_name is "Ron Clements"
    assert repr(movie.director) == "<Director Ron Clements>"

    actors = [Actor("Auli'i Cravalho"), Actor("Dwayne Johnson"), Actor("Rachel House"), Actor("Temuera Morrison")]
    for actor in actors:
        movie.add_actor(actor)
    assert repr(
        movie.actors) == "[<Actor Auli\'i Cravalho>, <Actor Dwayne Johnson>, <Actor Rachel House>, <Actor Temuera Morrison>]"

    genres = [Genre("Animated"), Genre("Comedy")]
    for genre in genres:
        movie.add_genre(genre)
    assert repr(
        movie.genres) == "[<Genre Animated>, <Genre Comedy>]"
def test_movie_delete_stuff():
    movie = Movie("Moana", 2016)
    movie.description = "   This is a movie   "
    assert movie.description == "This is a movie"
    movie.director = Director("Ron Clements")
    assert movie.director.director_full_name is "Ron Clements"
    assert repr(movie.director) == "<Director Ron Clements>"

    actors = [Actor("Auli'i Cravalho"), Actor("Dwayne Johnson"), Actor("Rachel House"), Actor("Temuera Morrison")]
    for actor in actors:
        movie.add_actor(actor)
    assert repr(
        movie.actors) == "[<Actor Auli\'i Cravalho>, <Actor Dwayne Johnson>, <Actor Rachel House>, <Actor Temuera Morrison>]"
    movie.remove_actor(Actor("Dwayne Johnson"))
    assert repr(
        movie.actors) == "[<Actor Auli\'i Cravalho>, <Actor Rachel House>, <Actor Temuera Morrison>]"
    movie.remove_actor(Actor("Jack Black"))
    assert repr(
        movie.actors) == "[<Actor Auli\'i Cravalho>, <Actor Rachel House>, <Actor Temuera Morrison>]"

    genres = [Genre("Animated"), Genre("Comedy")]
    for genre in genres:
        movie.add_genre(genre)
    assert repr(
        movie.genres) == "[<Genre Animated>, <Genre Comedy>]"
    movie.remove_genre(Genre("Comedy"))
    assert repr(
        movie.genres) == "[<Genre Animated>]"
def test_movie_runtime():
    movie = Movie("Moana", 2016)
    movie.description = "   This is a movie   "
    assert movie.description == "This is a movie"
    movie.director = Director("Ron Clements")
    assert movie.director.director_full_name is "Ron Clements"
    assert repr(movie.director) == "<Director Ron Clements>"

    actors = [Actor("Auli'i Cravalho"), Actor("Dwayne Johnson"), Actor("Rachel House"), Actor("Temuera Morrison")]
    for actor in actors:
        movie.add_actor(actor)
    assert repr(
        movie.actors) == "[<Actor Auli\'i Cravalho>, <Actor Dwayne Johnson>, <Actor Rachel House>, <Actor Temuera Morrison>]"
    movie.remove_actor(Actor("Dwayne Johnson"))
    assert repr(
        movie.actors) == "[<Actor Auli\'i Cravalho>, <Actor Rachel House>, <Actor Temuera Morrison>]"

    genres = [Genre("Animated"), Genre("Comedy")]
    for genre in genres:
        movie.add_genre(genre)
    assert repr(
        movie.genres) == "[<Genre Animated>, <Genre Comedy>]"
    movie.remove_genre(Genre("Comedy"))
    assert repr(movie.genres) == "[<Genre Animated>]"

    movie.runtime_minutes = 100
    assert movie.runtime_minutes is 100

def test_movie_init_full():
    movie = Movie("Moana", 2016)
    assert repr(movie) == "<Movie Moana, 2016>"

    director = Director("Ron Clements")
    movie.director = director
    assert repr(movie.director) == "<Director Ron Clements>"

    actors = [Actor("Auli'i Cravalho"), Actor("Dwayne Johnson"), Actor("Rachel House"), Actor("Temuera Morrison")]
    for actor in actors:
        movie.add_actor(actor)
    assert repr(
        movie.actors) == "[<Actor Auli\'i Cravalho>, <Actor Dwayne Johnson>, <Actor Rachel House>, <Actor Temuera Morrison>]"

    movie.runtime_minutes = 107
    assert ("Movie runtime: {} minutes".format(movie.runtime_minutes)) == "Movie runtime: 107 minutes"

def test_movie_eq():
    movie1 = Movie("Moana", 2016)
    movie2 = Movie("Moana", 2016)
    assert (movie1 == movie2) is True

def test_movie_lt(): #valid
    movie1 = Movie("Abc", 2016)
    movie2 = Movie("Moana", 1916)
    assert (movie1 < movie2) is True
def test_movie_lt_2(): #valid
    movie1 = Movie("Moana", 1916)
    movie2 = Movie("Moana", 2016)
    assert (movie1 < movie2) is True
def test_movie_lt_3(): #valid
    movie1 = Movie("Moana", 1916)
    movie2 = Movie("Moansa", 1916)
    assert (movie1 < movie2) is True
def test_movie_lt_4():
    movie1 = Movie("Moana", 1958)
    movie2 = Movie("AMoana", 2016)
    assert (movie1 < movie2) is False

def test_movie_director_handling():
    movie1 = Movie("Moana", 1916)
    movie1.director = Director("as")
    movie1.director = Director("asb")
    assert repr(movie1.director) == "<Director asb>"

#Movie File CSV Reader
def test_movie_file_csv_reader():
    filename = 'tests/data/Data1000Movies.csv'
    movie_file_reader = MovieFileCSVReader(filename)
    movie_file_reader.read_csv_file()

    assert len(movie_file_reader.dataset_of_movies) == 1000
    assert len(movie_file_reader.dataset_of_actors) == 1985
    assert len(movie_file_reader.dataset_of_directors) == 644
    assert len(movie_file_reader.dataset_of_genres) == 20

    all_movies_sorted = sorted(movie_file_reader.dataset_of_movies)
    print(f'first 3 unique directors of sorted dataset: {all_movies_sorted[0:3]}')
    all_actors_sorted = sorted(movie_file_reader.dataset_of_actors)
    print(f'first 3 unique directors of sorted dataset: {all_actors_sorted[0:3]}')
    all_directors_sorted = sorted(movie_file_reader.dataset_of_directors)
    print(f'first 3 unique directors of sorted dataset: {all_directors_sorted[0:3]}')
    all_genres_sorted = sorted(movie_file_reader.dataset_of_genres)
    print(f'first 3 unique directors of sorted dataset: {all_genres_sorted[0:3]}')
#Review:
def test_review():
    movie = Movie("Moana", 2016)
    review_text = "This movie was very enjoyable."
    rating = 8
    review1 = Review(movie, review_text, rating)
    review2 = Review(movie, review_text, rating)
    review3 = Review(movie, review_text, 0)
    review4 = Review(movie, review_text, 11)

    print(review1.movie)
    print("Review: {}".format(review1.review_text))
    print("Rating: {}".format(review1.rating))
    print("Timestamp1: {}".format(review1.timestamp))
    print("Timestamp2: {}".format(review2.timestamp))
    print(review1 == review2)

    print(review1)
    print(review2)
    print(review3)
    print(review4)

#User
def test_user():  # add movie
    user1 = User('  Martin   ', 'pw12345')
    print(user1.user_name)

    user1 = User('Martin', 'pw12345')
    user2 = User('Ian', 'pw67890')
    user3 = User('Daniel', 'pw87465')
    print(user1)
    print(user2)
    print(user3)

    movie1 = Movie("Up", 2009)
    movie1.runtime_minutes = 150
    user1.watch_movie(movie1)
    user1.watch_movie(movie1)
    print("Watched Movies:", user1.watched_movies)
    print("Watching  Time:", user1.time_spent_watching_movies_minutes)

    review1 = Review(movie1, "test", 5)
    user1.add_review(review1)
    user1.add_review(review1)

    print(user1.reviews)

#Watchlist
def test_watchlist_first_test(): #add movie
    watchlist = WatchList()
    print(f"Size of watchlist: {watchlist.size()}")
    #assert watchlist.size() == 0
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
    print(watchlist.first_movie_in_watchlist())
    #assert watchlist.first_movie_in_watchlist() == Movie("Moana", 2016)

def test_watchlist_remove():
    watchlist = WatchList()
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
    watchlist.remove_movie(Movie("Moana", 2016))
    print(watchlist.first_movie_in_watchlist())
    assert watchlist.first_movie_in_watchlist() == Movie("Ice Age", 2002)

def test_watchlist_valid_select():
    watchlist = WatchList()
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
    print(watchlist.select_movie_to_watch(1))
    assert watchlist.select_movie_to_watch(1) == Movie("Ice Age", 2002)

def test_watchlist_invalid_select():
    watchlist = WatchList()
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
    print(watchlist.select_movie_to_watch(3))
    assert watchlist.select_movie_to_watch(3) == None

def test_watchlist_size():
    watchlist = WatchList()
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
    print(watchlist.size())
    assert watchlist.size() == 3

def test_watchlist_first_movie_valid():
    watchlist = WatchList()
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
    print(watchlist.first_movie_in_watchlist())
    assert watchlist.first_movie_in_watchlist() == Movie("Moana", 2016)

def test_watchlist_first_movie_invalid():
    watchlist = WatchList()
    print(watchlist.first_movie_in_watchlist())
    assert watchlist.first_movie_in_watchlist() == None

def test_watchlist_add_same_movie():
    watchlist = WatchList()
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist_iter = iter(watchlist)
    print(next(watchlist_iter))
    print(next(watchlist_iter))
    #print(next(watchlist_iter))

def test_watchlist_remove_movie_not_in_watchlist():
    watchlist = WatchList()
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist.remove_movie(Movie("Guardians of the Galaxy", 2012))
    watchlist_iter = iter(watchlist)
    print(next(watchlist_iter))
    print(next(watchlist_iter))
    #print(next(watchlist_iter))

def test_watchlist_iter_invalid():
    watchlist = WatchList()
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Ice Age", 2002))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))

    watchlist_iter = iter(watchlist)
    while True:
        try:
            result = next(watchlist_iter)
        except StopIteration:
            break
        else:
            print(result)

#Watching Simulator
def test_watching_sim_add_review():
    a = MovieWatchingSimulation()
    movie1 = Movie("Moana", 2016)
    movie2 = Movie("Ice Age", 2002)
    movie3 = Movie("Guardians of the Galaxy", 2012)
    user1 = User('Jack', 'pw12345')
    user2 = User('James', 'pw67890')
    user3 = User('Janice', 'pw87465')
    review1 = Review(movie1, "Was good", 6)
    review2 = Review(movie1, "Average", 5)
    review3 = Review(movie1, "Very Great", 8)
    review4 = Review(movie2, "Great", 7)
    review5 = Review(movie2, "Excellent", 9)
    review6 = Review(movie3, "Boring", 3)

    a.add_movie_review(review1.movie, user1, review1.rating)
    a.add_movie_review(review2.movie, user2, review2.rating)
    a.add_movie_review(review3.movie, user3, review3.rating)
    a.add_movie_review(review4.movie, user1, review4.rating)
    a.add_movie_review(review5.movie, user2, review5.rating)
    a.add_movie_review(review6.movie, user1, review6.rating)
    a.add_movie_review(review4.movie, user1, review4.rating)

    assert a.movie_dict == {movie1: [[user1, 6], [user2, 5], [user3, 8]], movie2: [[user1, 7], [user2, 9], [user1, 7]], movie3: [[user1, 3]]}

def test_watching_sim_review_average():
    a = MovieWatchingSimulation()
    movie1 = Movie("Moana", 2016)
    movie2 = Movie("Ice Age", 2002)
    movie3 = Movie("Guardians of the Galaxy", 2012)
    user1 = User('Jack', 'pw12345')
    user2 = User('James', 'pw67890')
    user3 = User('Janice', 'pw87465')
    review1 = Review(movie1, "Was good", 6)
    review2 = Review(movie1, "Average", 5)
    review3 = Review(movie1, "Very Great", 8)
    review4 = Review(movie2, "Great", 7)
    review5 = Review(movie2, "Excellent", 9)
    review6 = Review(movie3, "Boring", 3)

    a.add_movie_review(review1.movie, user1, review1.rating)
    a.add_movie_review(review2.movie, user2, review2.rating)
    a.add_movie_review(review3.movie, user3, review3.rating)
    a.add_movie_review(review4.movie, user1, review4.rating)
    a.add_movie_review(review5.movie, user2, review5.rating)
    a.add_movie_review(review6.movie, user1, review6.rating)