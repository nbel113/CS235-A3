from flask import Blueprint, render_template, url_for, request, redirect
import math

import movie_web_app.a_adapters.repository as repo
from movie_web_app.a_adapters import database_repository

movies_blueprint = Blueprint(
    'movies_bp', __name__
)

@movies_blueprint.route('/list', methods=['GET'])
def list_movies():
    movies_per_page = 15
    # Read query parameters.
    page_num = request.args.get('page_num')

    if page_num is None:
        return redirect(url_for('movies_bp.list_movies', page_num=1))

    if page_num is not None:
        # Convert page_num from string to int.
        page_num = int(page_num)

    movie_list = repo.repo_instance.get_all_movies() #with database, points to it's get_all_movies
    last_page = math.ceil(len(movie_list) / movies_per_page)
    if (page_num < 1 or page_num > last_page):
        return redirect(url_for('movies_bp.list_movies', page_num=1))

    first_page_url = None
    prev_page_url = None
    next_page_url = None
    last_page_url = None

    page_total = (page_num - 1) * movies_per_page

    listing = movie_list[page_total:page_total + movies_per_page]

    repo_used = None

    for i in listing:
        try:                        #if using database
            director_full_name = repo.repo_instance.get_movie_director_full_name(i.directorID)
            
            i.director = director_full_name
            #print(i.director)

            actor_list = repo.repo_instance.get_movie_actors(i.movieID)
            i.actor_list = actor_list

            genre_list = repo.repo_instance.get_movie_genres(i.movieID)
            i.genre_list = genre_list

            repo_used = "database"

        except AttributeError:      #if using memory
            repo_used = "memory"
            break

    if page_num > 1:
        first_page_url = url_for('movies_bp.list_movies', page_num=1)
        prev_page_url = url_for('movies_bp.list_movies',  page_num=page_num - 1)

    if (page_num * movies_per_page) < len(movie_list):
        next_page_url = url_for('movies_bp.list_movies', page_num=page_num + 1)
        last_page_url = url_for('movies_bp.list_movies', page_num=last_page)

    return render_template(
        'movies/list_movies.html',
        page_num=page_num,
        last_page=last_page,
        listing=listing,
        repo_used=repo_used,
        page_total=page_total,
        movies_per_page=movies_per_page,
        movie_list_length=len(movie_list),

        first_page_url=first_page_url,
        prev_page_url=prev_page_url,
        next_page_url=next_page_url,
        last_page_url=last_page_url,
        list_movies_url=url_for('movies_bp.list_movies', page_num=1)
    )

@movies_blueprint.route('/list/')
#If no number is provided for the movie list position, redirect the user to its first page
def list_movies_no_number():
    return redirect(url_for('movies_bp.list_movies', page_num=1))
