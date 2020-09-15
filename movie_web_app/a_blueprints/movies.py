from flask import Blueprint, render_template, url_for, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import math

import movie_web_app.a_adapters.repository as repo
from movie_web_app.a_adapters.movie_repository import MoviesRepository, populate, load_movies

from movie_web_app.domain.model import Director, Genre, Actor, Movie, Review, User, WatchList
from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from movie_web_app.activitysimulations.watchingsimulation import MovieWatchingSimulation


movies_blueprint = Blueprint(
    'movies_bp', __name__
)

@movies_blueprint.route('/list', methods=['GET'])
def list_movies():
    movies_per_page = 15

    # Read query parameters.
    page_num = request.args.get('page_num')

    if page_num is None:
        # No page_num query parameter, so initialise page_num to start at the beginning.
        page_num = 0
    else:
        # Convert cursor from string to int.
        page_num = int(page_num)

    movie_list = repo.repo_instance.get_movies()
    last_page = math.ceil(len(movie_list) / movies_per_page)
    if (page_num <= 0 or page_num > last_page):
        return redirect(url_for('movies_bp.list_movies', page_num=1))

    first_article_url = None
    prev_article_url = None
    next_article_url = None
    last_article_url = None

    page_total = (page_num - 1) * movies_per_page
    listing = movie_list[page_total:page_total + movies_per_page]
    
    if page_num > 1:
        prev_article_url = url_for('movies_bp.list_movies',  page_num=page_num - 1)
        first_article_url = url_for('movies_bp.list_movies', page_num=1)

    if (page_num * movies_per_page) < len(movie_list):
        next_article_url = url_for('movies_bp.list_movies', page_num=page_num + 1)
        last_article_url = url_for('movies_bp.list_movies', page_num=last_page)


    return render_template(
        'movies/list_movies.html',
        page_num = page_num,
        last_page=last_page,
        listing = listing,
        page_total = page_total,
        movies_per_page=movies_per_page,
        movie_list_length=len(movie_list),

        first_article_url=first_article_url,
        last_article_url = last_article_url,
        next_article_url = next_article_url,
        prev_article_url = prev_article_url,
        list_movies_url = url_for('movies_bp.list_movies', page_num=1)
    )

@movies_blueprint.route('/list/')
#If no number is provided for the movie list position, redirect the user to its first page
def list_movies_no_number():
    return redirect(url_for('movies_bp.list_movies', page_num=1))
