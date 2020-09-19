from flask import Blueprint, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from password_validator import PasswordValidator

from functools import wraps

import movie_web_app.a_adapters.authen_repository as services
import movie_web_app.a_adapters.repository as repo

authen_blueprint = Blueprint(
    'authen_bp', __name__, url_prefix='/authen')

@authen_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    username_not_unique = None
    password_error_message = None

    if form.validate_on_submit():
        # Successful POST, i.e. the username and password have passed validation checking.
        # Use the service layer to attempt to add the new user.
        try:
            services.add_user(form.user_name.data, form.password.data, repo.repo_instance)
            # All is well, redirect the user to the login page.
            return redirect(url_for('authen_bp.login'))
        except services.NameNotUniqueException:
            username_not_unique = "Your username is already taken - please supply another"
    # For a GET or a failed POST request, return the Registration Web page.
    return render_template(
        'authen/credentials.html',
        title='Register',
        form=form,
        username_error_message=username_not_unique,
        password_error_message=password_error_message,
        handler_url=url_for('authen_bp.register'),
    )

@authen_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username_error_message = None
    password_error_message = None
    if form.validate_on_submit():
        # Successful POST, i.e. the username and password have passed validation checking.
        # Use the service layer to lookup the user.
        try:
            user = services.get_user(form.user_name.data, repo.repo_instance)
            # Authenticate user.
            services.authenticate_user(user['user_name'], form.password.data, repo.repo_instance)
            # Initialise session and redirect the user to the home page.
            session.clear()
            session['user_name'] = user['user_name']
            return redirect(url_for('home_bp.home'))
        except services.UnknownUserException:
            # Username not known to the system, set a suitable error message.
            username_error_message = 'Username not recognised - please supply another'
        except services.AuthenticationException:
            # Authentication failed, set a suitable error message.
            password_error_message = 'Password does not match supplied username - please check and try again'

    # For a GET or a failed POST, return the Login Web page.
    return render_template(
        'authen/credentials.html',
        title='Login',
        username_error_message=username_error_message,
        password_error_message=password_error_message,
        form=form,
    )

@authen_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))
def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_name' not in session:
            return redirect(url_for('authen_bp.login'))
        return view(**kwargs)
    return wrapped_view
"""
class NameIsNew:
    def __init__(self, message=None):
        if not message:
            message = u'Your username is already taken - please supply another'
        self.message = message
    def __call__(self, form, field):
        try:
            services.add_user(form.user_name.data, form.password.data, repo.repo_instance)
            return redirect(url_for('authen_bp.login'))
        except services.NameNotUniqueException:
            raise ValidationError(self.message)
"""
class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 8 characters, and contain an upper case letter, \
            a lower case letter and a digit'
        self.message = message
    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)

class RegistrationForm(FlaskForm):
    user_name = StringField('Username', validators = [
        DataRequired(),
        Length(min=3, message='Your username is too short')
    ])
    password = PasswordField('Password', validators = [
        DataRequired(),
        #NameIsNew(),
        PasswordValid(),
    ])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    user_name = StringField([
        DataRequired()])
    password = PasswordField([
        DataRequired()])
    submit = SubmitField('Login')