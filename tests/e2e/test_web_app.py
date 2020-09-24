import pytest
from flask import session
from movie_web_app.domain.model import Director, Genre, Actor, Movie, Review, TempReview, User, WatchList

#home
def test_home(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'Home  - CS235 Flix' in response.data

#list movies
def test_movies_list(client):
    # Check that we can retrieve the movies list page.
    response = client.get('/list?page_num=1')
    assert response.status_code == 200
    assert b'Page 1 - Movie List - CS235 Flix' in response.data

def test_movies_list_no_number(client):
    # Check that we can redirect to the first page of the movies list if no number is provided.
    response = client.get('/list/')
    assert response.status_code == 302
    assert b'Redirecting...' in response.data

def test_movies_list_zero_number(client):
    # Check that we can redirect to the first page of the movies list if 0 is provided.
    response = client.get('/list?page_num=0')
    assert response.status_code == 302
    assert b'Redirecting...' in response.data

def test_movies_list_negative_number(client):
    # Check that we can redirect to the first page of the movies list if a negative number is provided.
    response = client.get('/list/?page_num=-10')
    assert response.status_code == 302
    assert b'Redirecting...' in response.data

def test_movies_list_index_out_of_bounds(client):
    # Check that we can redirect to the first page of the movies list if page is provided.
    # Note that there are 15 movies per page, so with 1000 movies, there's a maximum of 67 pages
    response = client.get('/list/?page_num=100')
    assert response.status_code == 302
    assert b'Redirecting...' in response.data

#search
def test_search(client):
    # Check that we can retrieve the search page.
    response = client.get('/search')
    assert response.status_code == 200
    assert b'Search - CS235 Flix' in response.data

#auth
def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authen/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid username and password.
    response = client.post(
        '/authen/register',
        data={
            'user_name': 'qwerty',
            'password': '123Qweasd'
        }
    )
    #After sucessfully registering, the web app redirects the user to the login page
    assert response.headers['Location'] == 'http://localhost/authen/login'

@pytest.mark.parametrize(('user_name', 'password', 'message'), ( #may expand
        ('', '', b'Your username is required.'),
        ('cj', '', b'Your username is too short.'),
        ('test', '', b'Your password is required.'),
        ('test', 'test', b'Your password is invalid, please refer to Account notes.'),
        ('asdfgh', '123Qweasd', b'Your username is already taken - please supply another.'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/authen/register',
        data={'user_name': user_name, 'password': password}
    )
    #print(message)
    #print(response.data)

    assert message in response.data

def test_login(client, authen):
    # Check that we can retrieve the login page.
    status_code = client.get('/authen/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = authen.login()
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['user_name'] == 'asdfgh'

def test_logout(client, authen):
    # Login a user.
    authen.login()

    with client:
        # Check that logging out clears the user's session.
        authen.logout()
        assert 'user_id' not in session

#reviews
def test_login_required_to_see_reviews(client):
    response = client.post('/reviews')
    #redirect to the login page
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/authen/login'
def test_login_required_to_create_review(client):
    response = client.post('/create_review')
    #redirect to the login page
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/authen/login'
def test_login_required_to_edit_review(client):
    response = client.post('/edit_review')
    #redirect to the login page
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/authen/login'
def test_login_required_to_delete_review(client):
    response = client.post('/delete_review')
    #redirect to the login page
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/authen/login'

def test_create_review(client, authen):
    # Login a user.
    authen.login()
    # Check that if we don't provide create_review with this user's username, it just redirects us to the reviews listing page
    response = client.get('/create_review')
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/reviews'

    # Check that we can retrieve the create_review page for this user.
    response = client.get('/create_review?user=asdfgh')
    assert response.status_code == 200

    # Check that we can successfully create a review by supplying a valid movie title, review text, and rating
    response = client.post(
        '/create_review?user=asdfgh',
        data={
            'movie_title': 'Star Trek',
            'review_text': 'This is a review',
            'rating': 7
        }
    )
    assert response.headers['Location'] == 'http://localhost/reviews'

@pytest.mark.parametrize(('movie_title', 'review_text', 'rating', 'messages'), (
        ('', '', None,
            (b'Please provide a movie title for your review.',
             b'Please provide some text for your review.',
             b'Please provide an integer for your review rating.'
            )
        ),
        ('notamovie', '', None,
            (b'This is not a movie in the system.',
             b'Please provide some text for your review.',
             b'Please provide an integer for your review rating.'
            )
        ),
        ('Star Trek', 'fuck', None,
            (b'Your review contains profanity.',
             b'Please provide an integer for your review rating.'
            )
        ),
        ('Star Trek', 'text', 0,
            (
             b'Your review rating is out of range (1-10 inclusive).'
            )
        ),
        ('Star Trek', 'fuck', 5,
            (
             b'Your review contains profanity.'
            )
        ),
        ('notamovie', 'text', 5,
            (
             b'This is not a movie in the system.'
            )
        ),

))
def test_create_review_with_invalid_input(client, authen, movie_title, review_text, rating, messages):
    # Login a user.
    authen.login()

    # Check that we can retrieve the create_review page for this user.
    response = client.get('/create_review?user=asdfgh')
    assert response.status_code == 200

    # Attempt to comment on an article.
    response = client.post(
        '/create_review?user=asdfgh',
        data={
            'movie_title': movie_title,
            'review_text': review_text,
            'rating': rating
        }
    )
    #print(response.data)

    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response.data

def test_edit_review(client, authen):
    # Login a user.
    authen.login()
    # Check that if we don't provide create_review with this user's username, it just redirects us to the reviews listing page
    response = client.get('/create_review')
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/reviews'

    # Check that we can retrieve the create_review page for this user.
    response = client.get('/create_review?user=asdfgh')
    assert response.status_code == 200

    # Check that we can successfully create a review by supplying a valid movie title, review text, and rating
    response1 = client.post(
        '/create_review?user=asdfgh',
        data={
            'movie_title': 'Star Trek',
            'review_text': 'This is a review',
            'rating': 7
        }
    )
    assert response1.headers['Location'] == 'http://localhost/reviews'

    # Next, check that the review has been added by returning back to the reviews page
    # We know this is the case if the edit button for it is available, in which case we
    # access said button's link
    response2 = client.get('/reviews?page_num=1')
    a = str(response2.data).find("/edit_review?user=asdfgh&amp;review_id=")
    b = str(response2.data)[a:].find("\'")
    # print(b)
    link = str(response2.data)[a:a + b - 1]
    link = link.replace("&amp;", "&")
    #print(link)

    # Next, access the edit page, provide values for the fields, and 'press' the Submit button to edit the review.
    response3 = client.post(
        link,
        data={
            'movie_title': 'Split',
            'review_text': 'This is an edited review',
            'rating': 3,
            'submit_button': True #pressing the submit button
        }
    )
    response4 = client.get('/reviews?page_num=1')
    #print(response4.data)
    assert b'Split' in response4.data
    assert b'This is an edited review' in response4.data
    assert b'3' in response4.data

def test_edit_review_just_one_field(client, authen):
    # Login a user.
    authen.login()
    # Check that if we don't provide create_review with this user's username, it just redirects us to the reviews listing page
    response = client.get('/create_review')
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/reviews'

    # Check that we can retrieve the create_review page for this user.
    response = client.get('/create_review?user=asdfgh')
    assert response.status_code == 200

    # Check that we can successfully create a review by supplying a valid movie title, review text, and rating
    response1 = client.post(
        '/create_review?user=asdfgh',
        data={
            'movie_title': 'Star Trek',
            'review_text': 'This is a review',
            'rating': 7
        }
    )
    assert response1.headers['Location'] == 'http://localhost/reviews'

    # Next, check that the review has been added by returning back to the reviews page
    # We know this is the case if the edit button for it is available, in which case we
    # access said button's link
    response2 = client.get('/reviews?page_num=1')
    a = str(response2.data).find("/edit_review?user=asdfgh&amp;review_id=")
    b = str(response2.data)[a:].find("\'")
    # print(b)
    link = str(response2.data)[a:a + b - 1]
    link = link.replace("&amp;", "&")
    #print(link)

    # Next, access the edit page, provide values for the fields, and 'press' the Submit button to edit the review.
    response3 = client.post(
        link,
        data={
            'movie_title': '',
            'review_text': 'This is an edited review',
            'rating': '',
            'submit_button': True #pressing the submit button
        }
    )
    response4 = client.get('/reviews?page_num=1')
    #print(response4.data)
    assert b'Star Trek' in response4.data
    assert b'This is an edited review' in response4.data
    assert b'7' in response4.data


@pytest.mark.parametrize(('movie_title', 'review_text', 'rating', 'submit_button', 'messages'), (
        ('notamovie', '', '', True,
            (b'This is not a movie in the system.',
            )
        ),
        ('', 'fuck', '', True,
            (b'Your review contains profanity.',
            )
        ),
        ('', '', 0, True,
            (
             b'Your review rating is out of range (1-10 inclusive).'
            )
        ),
        ('', '', 'd', True,
            (
             b'Please provide an integer for your review rating.'
            )
        ),
        ('notamovie', 'fuck', 0, True,
            (
             b'This is not a movie in the system.',
             b'Your review contains profanity.',
             b'Your review rating is out of range (1-10 inclusive).'
            )
        ),
        ('notamovie', 'fuck', 'd', True,
            (
             b'This is not a movie in the system.',
             b'Your review contains profanity.',
             b'Please provide an integer for your review rating.'
            )
        ),
))
def test_edit_review_with_invalid_input(client, authen, movie_title, review_text, rating, submit_button, messages):
    # Login a user.
    authen.login()
#Create review
    # Check that if we don't provide create_review with this user's username, it just redirects us to the reviews listing page
    response = client.get('/create_review')
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/reviews'

    # Check that we can retrieve the create_review page for this user.
    response = client.get('/create_review?user=asdfgh')
    assert response.status_code == 200

    # Check that we can successfully create a review by supplying a valid movie title, review text, and rating
    response1 = client.post(
        '/create_review?user=asdfgh',
        data={
            'movie_title': 'Star Trek',
            'review_text': 'This is a review',
            'rating': 7
        }
    )
    assert response1.headers['Location'] == 'http://localhost/reviews'
# Edit review
    # Next, check that the review has been added by returning back to the reviews page
    # We know this is the case if the edit button for it is available, in which case we
    # access said button's link
    response2 = client.get('/reviews?page_num=1')
    a = str(response2.data).find("/edit_review?user=asdfgh&amp;review_id=")
    b = str(response2.data)[a:].find("\'")
    # print(b)
    link = str(response2.data)[a:a + b - 1]
    link = link.replace("&amp;", "&")
    #print(link)

    # Next, access the edit page, provide values for the fields, and 'press' the Submit button to edit the review.
    response3 = client.post(
        link,
        data={
            'movie_title': movie_title,
            'review_text': review_text,
            'rating': rating,
            'submit_button': submit_button
        }
    )

    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response3.data

def test_delete_review(client, authen):
    # Login a user.
    authen.login()

    # Check that we can successfully create a review by supplying a valid movie title, review text, and rating
    response1 = client.post(
        '/create_review?user=asdfgh',
        data={
            'movie_title': 'Star Trek',
            'review_text': 'This is a review',
            'rating': 7
        }
    )

    #Next, check that the review has been added by returning back to the reviews page
    #We know this is the case if the delete button for it is available, in which case we
    #access said button's link
    response2 = client.get('/reviews?page_num=1')
    a = str(response2.data).find("/delete_review?user=asdfgh&amp;review_id=")
    b = str(response2.data)[a:].find("\'")
    #print(b)
    link = str(response2.data)[a:a+b-1]
    link = link.replace("&amp;", "&")
    #print(link)

    #Next, access the delete page, and 'press' the Yes button to delete the review.
    response3 = client.post(
        link,
        data = {
            'yes_button': True #'pressing' the yes button
        }
    )
    #print(response3.data)

    #Finally, return back to the reviews listing page, so that we can check to see that
    #we deleted the review.
    response4 = client.get('/reviews?page_num=1')
    #print(response4.data)
    assert b'You have no reviews.' in response4.data
