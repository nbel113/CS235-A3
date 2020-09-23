from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from password_validator import PasswordValidator

from functools import wraps

import movie_web_app.a_adapters.authen_services as services
import movie_web_app.a_adapters.repository as repo

authen_blueprint = Blueprint(
    'authen_bp', __name__, url_prefix='/authen')

@authen_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    error_list = []
    form = RegistrationForm()
    if request.method == 'POST':

        #print(request.form['user_name'])

        try:
            user_name = form.user_name.data
            password = form.password.data
            if len(user_name) < 3:
                #print("a")
                if len(user_name) == 0:
                    error_list.append('Your username is required.')
                else:
                    error_list.append('Your username is too short.')
            schema = PasswordValidator()
            schema.min(8) \
                .has().uppercase() \
                .has().lowercase() \
                .has().digits()
            if not schema.validate(password):
                #print("b")
                if len(password) == 0:
                    error_list.append("Your password is required.")
                error_list.append('Your password is invalid, please refer to Account notes.')
            #print(error_list)
            if len(error_list) == 0:
                services.add_user(user_name, password, repo.repo_instance)
                # All is well, redirect the user to the login page.
                return redirect(url_for('authen_bp.login'))
            else:
                return render_template(
                    'authen/credentials.html',
                    title='Register',
                    form=form,
                    error_list=error_list,
                    handler_url=url_for('authen_bp.register'),
                )
        except services.NameNotUniqueException:
            error_list.append("Your username is already taken - please supply another.")
    # For a GET or a failed POST request, return the Registration Web page.
    return render_template(
        'authen/credentials.html',
        title='Register',
        form=form,
        error_list=error_list,
        handler_url=url_for('authen_bp.register'),
    )

@authen_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error_list = []
    form = LoginForm()
    if request.method == 'POST':
        # Successful POST, i.e. the username and password have passed validation checking.
        # Use the service layer to lookup the user.
        try:
            user = services.get_user(form.user_name.data, repo.repo_instance)
            services.authenticate_user(user['user_name'], form.password.data, repo.repo_instance)
            # Initialise session and redirect the user to the home page.
            session.clear()
            session['user_name'] = user['user_name']
            return redirect(url_for('home_bp.home'))
        except services.UnknownUserException:
            # Username not known to the system, set a suitable error message.
            error_list.append('Username not recognised - please supply another')
        except services.AuthenticationException:
            # Authentication failed, set a suitable error message.
            error_list.append('Password does not match supplied username - please check and try again')
    # For a GET or a failed POST, return the Login Web page.
    return render_template(
        'authen/credentials.html',
        title='Login',
        error_list=error_list,
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

class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 8 characters, and contain an upper case letter, a lower case letter and a digit'
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
        Length(min=3)
    ])
    password = PasswordField('Password', validators = [
        DataRequired(),
        PasswordValid(),
    ])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    user_name = StringField([
        DataRequired()])
    password = PasswordField([
        DataRequired()])
    submit = SubmitField('Login')