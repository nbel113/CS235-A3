from flask import Blueprint, render_template, request, redirect, url_for, session, make_response
from movie_web_app.a_blueprints.authen import login_required

from movie_web_app import *

import movie_web_app.a_adapters.repository as repo
import movie_web_app.a_adapters.review_services as review_services

from movie_web_app.a_adapters.repository import AbstractRepository
from movie_web_app.a_adapters.memory_repository import MemoryRepository
from movie_web_app.a_adapters.database_repository import *

from movie_web_app.domain.model import Director, Genre, Actor, Movie, Review, TempReview, User, WatchList
from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from movie_web_app.activitysimulations.watchingsimulation import MovieWatchingSimulation

from better_profanity import profanity
from flask_wtf import FlaskForm, Form
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired, ValidationError, NumberRange, Optional

import math

reviews_blueprint = Blueprint(
    'reviews_bp', __name__)

@reviews_blueprint.route('/reviews', methods=['GET', 'POST'])
@login_required
def reviews_by_user():

    repo_string = get_repo_string()

    reviews_per_page = 5
    page_num = request.args.get('page_num')

    if 'user_name' not in session: #if not in a user session
        #response = make_response()
        #response.headers['Location'] = 'authen/login'
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

    if repo_string == "memory":
        reviews_list = review_services.get_reviews_from_user(target_user, repo_inst)
    if repo_string == "database":
        reviews_list = repo_inst.get_reviews_from_user(target_user, repo_inst)

    last_page = math.ceil(len(reviews_list) / reviews_per_page)

    if (page_num < 1 or (page_num > last_page and last_page > 0)):
        return redirect(url_for('reviews_bp.reviews_by_user', page_num=1))

    first_page_url = None
    prev_page_url = None
    next_page_url = None
    last_page_url = None

    page_total = (page_num - 1) * reviews_per_page
    listing = reviews_list[page_total:page_total + reviews_per_page]

    if page_num > 1:
        first_page_url = url_for('reviews_bp.reviews_by_user', page_num=1)
        prev_page_url = url_for('reviews_bp.reviews_by_user', page_num=page_num - 1)

    if (page_num * reviews_per_page) < len(reviews_list):
        next_page_url = url_for('reviews_bp.reviews_by_user', page_num=page_num + 1)
        last_page_url = url_for('reviews_bp.reviews_by_user', page_num=last_page)

    list_of_review_delete_links = []
    for review in listing:
        review_delete_link = url_for('reviews_bp.delete_review', review=review)
        list_of_review_delete_links.append(review_delete_link)

    return render_template(
        'reviews/reviews.html',
        title='Reviews',
        user=target_user,
        reviews=reviews_list,

        page_num=page_num,
        last_page=last_page,
        listing=listing,
        repo_string=repo_string,
        page_total=page_total,
        movies_per_page=reviews_per_page,
        movie_list_length=len(reviews_list),
    
        first_page_url=first_page_url,
        last_page_url=last_page_url,
        next_page_url=next_page_url,
        prev_page_url=prev_page_url,
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
    error_list = []
    session_user_name = session['user_name']
    user_name = request.args.get('user')
    if 'user_name' not in session:
        return redirect(url_for('home_bp.home'))
    if user_name != session_user_name:
        return redirect(url_for('reviews_bp.reviews_by_user'))

    form = CreateReviewForm()
    repo_inst = repo.repo_instance
    user = repo_inst.get_user(user_name)

    if request.method == 'POST':
        movie_title = str(form.movie_title.data)
        movie = repo_inst.get_movie(str(form.movie_title.data))
        review_text = str(form.review_text.data)
        rating = form.rating.data

        if movie is None:
            if movie_title == "":
                error_list.append('Please provide a movie title for your review.')
            else:
                error_list.append('This is not a movie in the system.')
        if review_text == "":
            error_list.append('Please provide some text for your review.')
        if profanity.contains_profanity(review_text):
            error_list.append('Your review contains profanity.')
        if type(rating) == int:
            if int(rating) < 1 or int(rating) > 10:
                error_list.append('Your review rating is out of range (1-10 inclusive).')
        else:
            error_list.append('Please provide an integer for your review rating.')

        if len(error_list) == 0:
            review = Review(movie, review_text, int(rating))

            repo_inst.add_review(user, review)          #for database
            review_services.add_review(user, review)    #for memory
            return redirect(url_for('reviews_bp.reviews_by_user'))

    return render_template(
        'reviews/create_review.html',
        title='Create Review',
        form=form,
        review_url=url_for('reviews_bp.reviews_by_user'),
        error_list=error_list
    )

@reviews_blueprint.route('/edit_review', methods=['GET', 'POST'])
@login_required
def edit_review():
    repo_string = get_repo_string()

    error_list = []
    user_name = request.args.get('user')
    if 'user_name' not in session:
        return redirect(url_for('home_bp.home'))
    session_user_name = session['user_name']
    if user_name != session_user_name:
        return redirect(url_for('reviews_bp.reviews_by_user'))

    review_id = request.args.get('review_id')
    repo_inst = repo.repo_instance

    if repo_string == "memory":
        review = review_services.get_review_by_user_and_id(session_user_name, review_id, repo_inst)
    if repo_string == "database":
        review = repo_inst.get_review_by_user_and_id(session_user_name, review_id, repo_inst)

    # BASED ON:
        # davidism's answer to:
        # https://stackoverflow.com/questions/35774060/determine-which-wtforms-button-was-pressed-in-a-flask-view
    form = EditReviewForm()
    if request.method == 'POST':
        movie_title = str(form.movie_title.data)
        movie = repo_inst.get_movie(str(form.movie_title.data))
        review_text = form.review_text.data
        rating = form.rating.data

        if (movie is None) and movie_title != "":
            error_list.append('This is not a movie in the system.')

        if profanity.contains_profanity(review_text):
            error_list.append('Your review contains profanity.')

        #print(rating)
        if rating != "":
            try:
                if int(rating) < 1 or int(rating) > 10:
                    error_list.append('Your review rating is out of range (1-10 inclusive).')
            except ValueError:
                error_list.append('Please provide an integer for your review rating.')
        #print(error_list)
        if form.submit_button.data and len(error_list) == 0:
            new_review = TempReview(movie, review_text, rating)

            if repo_string == "memory":
                review_services.edit_review(review, new_review)
            if repo_string == "database":
                repo_inst.edit_review(review, new_review)

            #print(new_review.timestamp)
            return redirect(url_for('reviews_bp.reviews_by_user'))

    return render_template(
        'reviews/edit_review.html',
        title='Edit Review',
        review=review,
        form=form,
        review_url=url_for('reviews_bp.reviews_by_user'),
        error_list=error_list
    )

@reviews_blueprint.route('/delete_review', methods=['GET', 'POST'])
@login_required
def delete_review():
    repo_string = get_repo_string()
    session_user_name = session['user_name']
    user_name = request.args.get('user')
    if user_name != session_user_name:
        return redirect(url_for('reviews_bp.reviews_by_user'))

    review_id = request.args.get('review_id')
    repo_inst = repo.repo_instance

    # if the user goes back to the delete page of an already deleted/non-existent review, they get redirected back to the reviews page.
    if repo_string == "memory":
        if review_services.get_review_by_user_and_id(session_user_name, review_id, repo_inst) is None:
            return redirect(url_for('reviews_bp.reviews_by_user'))
        review = review_services.get_review_by_user_and_id(session_user_name, review_id, repo_inst)

    if repo_string == "database":
        if repo_inst.get_review_by_user_and_id(session_user_name, review_id, repo_inst) is None:
            return redirect(url_for('reviews_bp.reviews_by_user'))
        review = repo_inst.get_review_by_user_and_id(session_user_name, review_id, repo_inst)

    # BASED ON:
        # davidism's answer to:
        # https://stackoverflow.com/questions/35774060/determine-which-wtforms-button-was-pressed-in-a-flask-view
    form = DeleteReviewForm()

    if request.method == 'POST':
        if form.yes_button.data:
            if repo_string == "memory":
                review_services.delete_review(session_user_name, review, repo_inst)
            if repo_string == "database":
                repo_inst.delete_review(session_user_name, review, repo_inst)
            return redirect(url_for('reviews_bp.reviews_by_user'))
        elif form.no_button.data:
            return redirect(url_for('reviews_bp.reviews_by_user'))
    return render_template(
        'reviews/delete_review.html',
        title='Delete Review',
        review=review,
        form=form,
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

class CreateReviewForm(FlaskForm):
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

#BASED ON:
    #davidism's answer to:
    #https://stackoverflow.com/questions/35774060/determine-which-wtforms-button-was-pressed-in-a-flask-view
class EditReviewForm(FlaskForm):
    movie_title = StringField(validators=[
        Optional(strip_whitespace=True),
        #DataRequired(message="Please provide a movie title."),
    ])
    review_text = TextAreaField(validators=[
        Optional(strip_whitespace=True),
        #DataRequired(message="Please provide text for your review."),
        ProfanityFree(message='Your review must not contain profanity.')
    ])
    #NOTE: for edit_review, rating is a string field, so that non-integer input isn't just set to None
    rating = StringField(validators=[
        #DataRequired(message="Ratings must be whole numbers between 1 to 10."),
        Optional(strip_whitespace=True),
        NumberRange(min=1, max=10, message='Ratings must be whole numbers between 1 to 10.')
    ])
    submit_button = SubmitField("Submit")

#BASED ON:
    #davidism's answer to:
    #https://stackoverflow.com/questions/35774060/determine-which-wtforms-button-was-pressed-in-a-flask-view
class DeleteReviewForm(FlaskForm):
    yes_button = SubmitField('Yes')
    no_button = SubmitField('No')