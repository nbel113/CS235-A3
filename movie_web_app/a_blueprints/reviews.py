from flask import Blueprint, flash, render_template, redirect, url_for, session, request
from movie_web_app.a_blueprints.authen import login_required

import movie_web_app.a_adapters.repository as repo
import movie_web_app.a_adapters.review_repository as review_repo

from movie_web_app.a_adapters.repository import AbstractRepository
from movie_web_app.domain.model import Director, Genre, Actor, Movie, Review, User, WatchList
from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from movie_web_app.activitysimulations.watchingsimulation import MovieWatchingSimulation

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError, NumberRange

import math

reviews_blueprint = Blueprint(
    'reviews_bp', __name__)

@reviews_blueprint.route('/reviews', methods=['GET'])
@login_required
def reviews_by_user():
    reviews_per_page = 5
    page_num = request.args.get('page_num')

    if 'user_name' not in session: #if not in a user session
        return redirect(url_for('home_bp.home'))
        #also need to prevent seeing other people's reviews

    if page_num is None:
        # No page_num query parameter, so initialise page_num to start at the beginning.
        page_num = 0
    else:
        # Convert page_num from string to int.
        page_num = int(page_num)

    repo_inst = repo.repo_instance
    target_user = session["user_name"]
    reviews_list = review_repo.get_reviews_from_user(target_user, repo_inst)

    last_page = math.ceil(len(reviews_list) / reviews_per_page)

    if (page_num < 1 or (page_num > last_page and last_page > 0)):
        return redirect(url_for('reviews_bp.reviews_by_user', page_num=1))

    first_article_url = None
    prev_article_url = None
    next_article_url = None
    last_article_url = None

    page_total = (page_num - 1) * reviews_per_page
    listing = reviews_list[page_total:page_total + reviews_per_page]

    if page_num > 1:
        first_article_url = url_for('reviews_bp.reviews_by_user', page_num=1)
        prev_article_url = url_for('reviews_bp.reviews_by_user', page_num=page_num - 1)

    if (page_num * reviews_per_page) < len(reviews_list):
        next_article_url = url_for('reviews_bp.reviews_by_user', page_num=page_num + 1)
        last_article_url = url_for('reviews_bp.reviews_by_user', page_num=last_page)

    return render_template(
        'reviews/reviews.html',
        title='Reviews',
        user=target_user,
        reviews=reviews_list,

        page_num=page_num,
        last_page=last_page,
        listing=listing,
        page_total=page_total,
        movies_per_page=reviews_per_page,
        movie_list_length=len(reviews_list),

        first_article_url=first_article_url,
        last_article_url=last_article_url,
        next_article_url=next_article_url,
        prev_article_url=prev_article_url,
        list_movies_url=url_for('reviews_bp.reviews_by_user', page_num=1),
        create_review_url = url_for('reviews_bp.create_review', user=target_user)
    )

@reviews_blueprint.route('/reviews/')
#If no number is provided for the movie list position, redirect the user to its first page
def reviews_by_user_no_number():
    return redirect(url_for('reviews_bp.reviews_by_user', page_num=1))

@reviews_blueprint.route('/create_review', methods=['GET', 'POST'])
@login_required
def create_review():
    movie_title_error_message = None
    display = False

    user_name = request.args.get('user')
    if 'user_name' not in session:
        return redirect(url_for('home_bp.home'))
    if user_name != session['user_name']:
        return redirect(url_for('reviews_bp.reviews_by_user'))
    form = ReviewForm()
    repo_inst = repo.repo_instance
    user = repo_inst.get_user(user_name)

    if form.validate_on_submit():
        movie = repo_inst.get_movie(str(form.movie_title.data))
        review_text = str(form.review_text.data)
        rating = int(form.rating.data)
        if movie is None:
            movie_title_error_message = 'This isn\'t a movie on the system.'
            display = True
        else:
            display = False
            review = Review(movie, review_text, rating)
            review_repo.add_review(user, review, repo_inst)
            return redirect(url_for('reviews_bp.reviews_by_user'))

    return render_template(
        'reviews/create_review.html',
        title='Create Review',
        form=form,
        display=display,
        movie_title_error_message = movie_title_error_message,
        review_url=url_for('reviews_bp.reviews_by_user'),
    )

class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity.'
        self.message = message
    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)

class ReviewForm(FlaskForm):
    movie_title = StringField(validators = [
        DataRequired(message="Please provide a movie title."),
    ])
    review_text = TextAreaField(validators = [
        DataRequired(message="Please provide text for your review."),
        ProfanityFree(message='Your review must not contain profanity.')
    ])
    rating = IntegerField(validators = [
        DataRequired(message="Ratings must be whole numbers between 1 to 10."),
        NumberRange(min=1, max=10, message='Ratings must be whole numbers between 1 to 10.')
    ])
    submit = SubmitField('Submit')

