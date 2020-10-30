from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.sql import *
from sqlalchemy.orm import mapper, relationship
from movie_web_app.domain.model import *

metadata = MetaData()

director = Table(
    'director', metadata,
    Column('directorID', Integer, primary_key=True, autoincrement=True),
    Column('director_full_name', String, nullable=False)
)
genre = Table(
    'genre', metadata,
    Column('genreID', Integer, primary_key=True, autoincrement=True),
    Column('genre_name', String, nullable=False)
)
actor = Table(
    'actor', metadata,
    Column('actorID', Integer, primary_key=True, autoincrement=True),
    Column('actor_full_name', String, nullable=False)
)
movie = Table(
    'movie', metadata,
    Column('movieID', Integer, primary_key=True, autoincrement=True),
    Column('directorID', Integer, ForeignKey('director.directorID')),
    Column('title', String, nullable=False),
    Column('release_year', Integer, nullable=False),
    Column('description', String, nullable=False),
    Column('runtime_minutes', Integer, nullable=False)
)
movie_genre = Table(
    'movie_genre', metadata,
    Column('movie_genreID', Integer, primary_key=True, autoincrement=True),
    Column('movieID', Integer, ForeignKey('movie.movieID')),
    Column('genreID', Integer, ForeignKey('genre.genreID'))
)
movie_actor = Table(
    'movie_actor', metadata,
    Column('movie_actorID', Integer, primary_key=True, autoincrement=True),
    Column('movieID', Integer, ForeignKey('movie.movieID')),
    Column('actorID', Integer, ForeignKey('actor.actorID'))
)
review = Table(
    'review', metadata,
    Column('reviewID', Integer, primary_key=True, autoincrement=True),
    Column('movieID', Integer, ForeignKey('movie.movieID')),
    Column('review_text', String, nullable=False),
    Column('rating', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=False),
    Column('latest_edit', DateTime, nullable=True)
)
user = Table(
    'user', metadata,
    Column('userID', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String, unique=True, nullable=False),
    Column('password', String, nullable=False),
    Column('time_spent_watching_movies_minutes', Integer, default=0)
)
user_review = Table(
    'user_review', metadata,
    Column('user_reviewID', Integer, primary_key=True, autoincrement=True),
    Column('reviewID', Integer, ForeignKey('review.reviewID')),
    Column('userID', Integer, ForeignKey('user.userID'))
)

def map_model_to_tables():
    #c = columns
    mapper(Director, director, properties={
        '_Director__director_full_name': director.c.director_full_name,
    })
    genre_mapper = mapper(Genre, genre, properties={
        '_Genre__genre_name': genre.c.genre_name,
    })
    actor_mapper = mapper(Actor, actor, properties={
        '_Actor__actor_full_name': actor.c.actor_full_name,
    })
    movie_mapper = mapper(Movie, movie, properties={
        #_Movie__actors and _Movie__genres can't be used
        '_Movie__actor_list': relationship(actor_mapper, secondary=movie_actor, backref='_movie'),
        '_Movie__genre_list': relationship(genre_mapper, secondary=movie_genre, backref='_movie'),
        '_Movie__title': movie.c.title,
        '_Movie__release_year': movie.c.release_year,
        '_Movie__description': movie.c.description,
        '_Movie__runtime_minutes': movie.c.runtime_minutes,
    })

    review_mapper = mapper(Review, review, properties={
        '_Review__movie': relationship(Movie, backref='_review'),
        '_Review__review_text': review.c.review_text,
        '_Review__rating': review.c.rating,
        '_Review__timestamp': review.c.timestamp,
        '_Review__latest_edit': review.c.latest_edit,
    })
    mapper(User, user, properties={
        '_User__reviews': relationship(review_mapper, secondary=user_review, backref='_user'),
        '_User__user_name': user.c.user_name,
        '_User__password': user.c.password,
        '_User__time_spent_watching_movies_minutes': user.c.time_spent_watching_movies_minutes,
    })