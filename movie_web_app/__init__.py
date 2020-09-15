"""Initialize Flask app."""
from flask import Flask
import os

import movie_web_app.a_adapters.repository as repo
from movie_web_app.a_adapters.movie_repository import MoviesRepository, populate

from movie_web_app.domain.model import Director, Genre, Actor, Movie, Review, User, WatchList
from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from movie_web_app.activitysimulations.watchingsimulation import MovieWatchingSimulation

def create_app(test_config=None):
    app = Flask(__name__)

    # Configure the app from configuration-file settings
    app.config.from_object('config.Config')
    data_path = os.path.join('movie_web_app', 'a_adapters', 'data')

    if test_config is not None:
        # Load test configuration, and override configuration settings
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    repo.repo_instance = MoviesRepository()
    populate(data_path, repo.repo_instance)

    with app.app_context():
        from .a_blueprints import home
        app.register_blueprint(home.home_blueprint)
        from .a_blueprints import movies
        app.register_blueprint(movies.movies_blueprint)

    return app