import csv
import os
import sqlite3

from datetime import date
from typing import List

from sqlalchemy import desc, asc, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug.security import generate_password_hash

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from movie_web_app.domain.model import *
from movie_web_app.a_adapters.repository import *
from movie_web_app.datafilereaders.movie_file_csv_reader import *
from movie_web_app.datafilereaders.user_file_csv_reader import *

tags = None

def populate(session_factory, data_path):
    movie_file_reader = MovieFileCSVReader(os.path.join(data_path, 'Data1000Movies.csv'))
    movie_file_reader.read_csv_file()

    user_file_reader = UserFileCSVReader(os.path.join(data_path, 'users.csv'))
    user_file_reader.read_csv_file()

    session = session_factory()
    # This takes all movies from the csv file (represented as domain model objects) and adds them to the
    # database. If the uniqueness of directors, actors, genres is correctly handled, and the relationships
    # are correctly set up in the ORM mapper, then all associations will be dealt with as well!

    for actor in movie_file_reader.dataset_of_actors:
        session.add(actor)

    for genre in movie_file_reader.dataset_of_genres:
        session.add(genre)

    for director in movie_file_reader.dataset_of_directors:
        session.add(director)

    for movie in movie_file_reader.dataset_of_movies:
        session.add(movie)

    for user in user_file_reader.dataset_of_users:
        session.add(user)

    session.commit()
    print("~~~First commit complete, now starting the second populate to obtain the relations~~~")

def second_populate(session_factory, data_path):
    movie_file_reader = MovieFileCSVReader(os.path.join(data_path, 'Data1000Movies.csv'))
    movie_file_reader.read_csv_file()

    user_file_reader = UserFileCSVReader(os.path.join(data_path, 'users.csv'))
    user_file_reader.read_csv_file()

    session = session_factory()
    # This takes all movies from the csv file (represented as domain model objects) and adds them to the
    # database. If the uniqueness of directors, actors, genres is correctly handled, and the relationships
    # are correctly set up in the ORM mapper, then all associations will be dealt with as well!


    movie_count = 1
    for movie in movie_file_reader.dataset_of_movies:
        for a in session.execute(
            "SELECT * \
            FROM director \
            WHERE director_full_name = \"" + str(movie.director) + "\";"
        ):
            session.execute(
                "UPDATE movie \
                SET directorID = \'" + str(a[0]) + "\' \
                WHERE movieID = \'" + str(movie_count) + "\';"
            )
            movie_file_reader.subset_of_movie_directors[str(movie.title)] = a

        for actor in movie.actors:
            for b in session.execute(
                "SELECT actorID \
                FROM actor \
                WHERE actor_full_name = \"" + str(actor) + "\";"
            ):
                session.execute(
                    "INSERT INTO movie_actor(movieID, actorID) \
                    VALUES (\'" + str(movie_count) + "\', \'" + str(b[0]) + "\');"
                )
                #print(actor, movie_count, b[0])

        for genre in movie.genres:
            for c in session.execute(
                "SELECT genreID \
                FROM genre \
                WHERE genre_name = \"" + str(genre) + "\";"
            ):
                session.execute(
                    "INSERT INTO movie_genre(movieID, genreID) \
                    VALUES (\'" + str(movie_count) + "\', \'" + str(c[0]) + "\');"
                )
                #print(genre, movie_count, c[0])

        movie_count += 1
    session.commit()

class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)
        self._movies = list()

    def close_session(self):
        self._session_cm.close_current_session()
    def reset_session(self):
        self._session_cm.reset_session()

    def add_movie(self, movie: Movie):
        with self._session_cm as scm:
            scm.session.add(movie)
            scm.commit()
    def get_movie(self, title: str) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session.query(Movie).filter_by(_Movie__title=title).one()
            #print("~~~~~~~~~~", movie)
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return movie
    def get_movie_info_by_id(self, movieID):
        movie_info = None
        try:
            for a in self._session_cm.session.execute(
                "SELECT * \
                FROM movie \
                WHERE movieID = \'" + str(movieID) + "\'"
            ):
                movie_info = a
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return movie_info

    def set_all_movies(self):
        all_movies = self._session_cm.session.query(Movie).all()
        for i in all_movies:
            director_full_name = self.get_movie_director_full_name(i.directorID)
            i.director = director_full_name

            actor_list = self.get_movie_actors(i.movieID)
            i.actor_list = actor_list

            genre_list = self.get_movie_genres(i.movieID)
            i.genre_list = genre_list

        return all_movies

    def get_all_movies(self):
        all_movies = self._session_cm.session.query(Movie).all()
        return all_movies

    def get_movie_director_full_name(self, directorID):
        director_full_name = None
        try:
            for a in self._session_cm.session.execute(
                "SELECT director_full_name \
                FROM director \
                WHERE directorID = \"" + str(directorID) + "\";"
            ):
                director_full_name = a[0]

        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return director_full_name

    def get_movie_actors(self, movieID):
        actor_list = []
        try:
            for a in self._session_cm.session.execute(
                "SELECT actor_full_name \
                FROM movie_actor \
                INNER JOIN actor \
                    USING(actorID) \
                WHERE movieID = \"" + str(movieID) + "\";"
            ):
                actor_list.append(a[0])

        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return actor_list

    def get_movie_genres(self, movieID):
        genre_list = []
        try:
            for a in self._session_cm.session.execute(
                "SELECT genre_name \
                FROM movie_genre \
                INNER JOIN genre \
                    USING(genreID) \
                WHERE movieID = \"" + str(movieID) + "\";"
            ):
                genre_list.append(a[0])

        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return genre_list

    def get_movies_by_search_title(self, title_search: str):
        title_search = title_search.strip().casefold()
        if title_search == '':
            return None
        titles_list = title_search.split(",")
        for i in range(len(titles_list)):
            titles_list[i] = titles_list[i].strip()
        #print(titles_list)
        results = []
        for movie in self.get_all_movies():
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
        for movie in self.get_all_movies():
            director_name = self.get_movie_director_full_name(movie.directorID)
            for i in range(len(directors_list)):
                if director_name.casefold().find(directors_list[i]) is not -1:  # if the text is a substring
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
        for movie in self.get_all_movies():
            movie_actor_list = self.get_movie_actors(movie.movieID)
            for i in range(len(actors_list)):
                for movie_actor in movie_actor_list:
                    if movie_actor.casefold().find(actors_list[i]) is not -1:  # if the text is a substring
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
        for movie in self.get_all_movies():
            movie_genre_list = self.get_movie_genres(movie.movieID)
            for i in range(len(genres_list)):
                for movie_genre in movie_genre_list:
                    if movie_genre.casefold().find(genres_list[i]) is not -1:  # if the text is a substring
                        results.append(movie)
        return results

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()
    def get_user(self, user_name) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter_by(_User__user_name=user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user
    def get_all_users(self):
        all_users = self._session_cm.session.query(User).all()
        return all_users

    def add_review(self, user: User, review: Review):
        with self._session_cm as scm:
            user.add_review(review)
            scm.session.add(review)
            #scm.session.execute
            scm.commit()
    def get_review(self, review_id) -> Review:
        review = None
        try:
            for a in self._session_cm.session.execute(
                "SELECT * \
                FROM review \
                WHERE reviewID = \'" + str(review_id) + "\'"
            ):
                movie_info = self.get_movie_info_by_id(a[1])

                movie = self.get_movie(movie_info[2])
                text = str(a[2])
                rating = int(a[3])

                review = Review(movie, text, rating)

        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return review
    def get_all_reviews(self):
        all_reviews = self._session_cm.session.query(Review).all()
        return all_reviews
    def get_reviews_from_user(self, user_name: str, repo: AbstractRepository):
        user = repo.get_user(user_name)
        if user is None:
            raise UnknownUserException
        return user.reviews

    def get_review_by_user_and_id(self, session_user_name: str, review_id, repo: AbstractRepository):
        user = repo.get_user(session_user_name)
        review = None
        try:
            for i in user.reviews:
                if str(i.reviewID) == str(review_id):
                    review = i


        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return review

    def edit_review(self, review: Review, new_review: TempReview):
        edit_occurred = False

        if not (new_review.movie is None or new_review.movie.title == ""):
            a = self.get_movie(new_review.movie.title)
            #try:
            review.movie_id = a.movieID

            #except AttributeError:
            review.movieID = a.movieID
            """
            for b in self._session_cm.session.execute(
                "SELECT reviewID \
                FROM review \
                WHERE reviewID = \"" + str(review.reviewID) + "\";"
            ):
                print("\t ~review.movieID", b, review.movieID)
            """
            self._session_cm.session.execute(
                "UPDATE review \
                SET movieID = \"" + str(review.movieID) + "\" \
                WHERE reviewID = \"" + str(review.reviewID) + "\";"
            )
            edit_occurred = True

        if not (new_review.review_text == "" or new_review.review_text is None):
            review.review_text = new_review.review_text
            """
            for b in self._session_cm.session.execute(
                "SELECT reviewID \
                FROM review \
                WHERE reviewID = \"" + str(review.reviewID) + "\";"
            ):
                print("\t ~review.review_text", b, review.review_text)
            """
            self._session_cm.session.execute(
                "UPDATE review \
                SET review_text = \"" + str(review.review_text) + "\" \
                WHERE reviewID = \"" + str(review.reviewID) + "\";"
            )
            edit_occurred = True

        if not (new_review.rating == "" or new_review.rating is None):
            review.rating = new_review.rating
            """
            for b in self._session_cm.session.execute(
                "SELECT reviewID \
                FROM review \
                WHERE reviewID = \"" + str(review.reviewID) + "\";"
            ):
                print("\t ~review.rating", b, review.rating)
            """
            self._session_cm.session.execute(
                "UPDATE review \
                SET rating = \"" + str(review.rating) + "\" \
                WHERE reviewID = \"" + str(review.reviewID) + "\";"
            )
            edit_occurred = True

        if edit_occurred:
            review.latest_edit = new_review.timestamp
            self._session_cm.session.execute(
                "UPDATE review \
                SET latest_edit = \"" + str(review.latest_edit) + "\" \
                WHERE reviewID = \"" + str(review.reviewID) + "\";"
            )
            self._session_cm.session.commit()

    def delete_review(self, session_user_name: str, review: Review, repo: AbstractRepository):
        user = repo.get_user(session_user_name)
        self._session_cm.session.execute(
            "DELETE FROM review \
            WHERE reviewID = \"" + str(review.reviewID) + "\";"
        )
        self._session_cm.session.execute(
            "DELETE FROM user_review \
            WHERE reviewID = \"" + str(review.reviewID) + "\";"
        )
        self._session_cm.session.commit()
        #return user.reviews.remove(review)


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory) #, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory) #, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if self.__session is not None:
            self.__session.close()
