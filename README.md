# CompSci 235 A3 - CS235Flix - nbel113

## Warning
Please ignore the latest commit from main
Please pull the latest commit from master, or the first commit from October 30th from main

## Description
Nigel Bell's submission for CompSci 235's Assignment 3, based on the course's skeleton Python project CS235Flix.

* This web application demonstrates the use of Python's Flask framework. 
* It makes use of libraries such as the Jinja templating library and WTForms. 
* Architectural design patterns and principles including Repository, Dependency Inversion and Single Responsibility have been used to design the application. 
* This also uses Flask Blueprints to maintain a separation of concerns between application functions. 
* Testing includes unit and end-to-end testing using the pytest tool. 

## Installation

**Installation via requirements.txt**

```shell
$ cd CS235-A3
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File'->'Settings' and select 'Project:CS235-A2' from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment. 

## Execution

**Running the application**

From the *CS235-A2* directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 


## Configuration

The *CS235-A2/.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.


## Testing
NOTE: Referring to https://piazza.com/class/kd3xeoxyktkby?cid=234, Run testing with:
```
python -m pytest
```


Testing requires that file *CS235-A3/tests/conftest.py* be edited to set the values of `TEST_DATA_PATH_MEMORY` and `TEST_DATA_PATH_DATABASE`. You should set these to the absolute paths of the *CS235-A3/tests/data/memory* and *CS235-A3/tests/data/database* respectively. 

E.g. 
`TEST_DATA_PATH_MEMORY = os.path.join('C:', os.sep, 'Users', 'nbel113', 'Documents', 'Python dev', 'CS235-A3', 'tests', 'data', 'memory')`

assigns TEST_DATA_PATH_MEMORY with the following value (the use of os.path.join and os.sep ensures use of the correct platform path separator):
`C:\Users\nbel113\Documents\python-dev\CS235-A3\tests\data\memory`

You can then run the tests.


# Notes:
* Searching by Director, Actor(s) and/or Genre(s) using 'Search movies' will be slower due to how it is implemented.
* When attempting the tests within tests\e2e\test_web_app, if:
    `'REPOSITORY': 'database'` and `'TEST_DATA_PATH': TEST_DATA_PATH_DATABASE` in conftest's client function, then the following error message occurs for all but it's first test:
`
sqlalchemy.exc.ArgumentError: Class '<class 'movie_web_app.domain.model.Director'>' already has a primary mapper defined. Use non_primary=True to create a non primary Mapper.  clear_mappers() will remove *all* current mappers from all classes.
`
    * It essentially means that since the there is already a primary mapper created (in movie_web_app/a_adapters/orm.py) by the first test's client, then we can't make duplicate primary mappers.
    * All these tests still pass when the web app is set to memory. 
    * When testing with the database, each test was individually tested, and does pass. The comment #DB-PASS is put next to tests that individually passed. 
    * This issue also occurs in the COVID web app's test_web_app tests too. 
* Even though the relationship between users and reviews is more naturally one-to-many (since a review is created by one user, and one user can make many reviews), I decided to add a user-review table to handle the relation separately, so that the user foreign key doesn't appear within the 'review' table.
    This is more faithful to the Review class in the model code, as it also lacks a variable/data structure relevant to the user.
    It also opens up the opportunity to further expand this web app to allow users to collaborate with reviews (eg users can have their copy of the review they collaborated in with other users).
* In UserReview, reviewID is the first foreign key, since it is usually more unique than userID.
* Testing takes roughly 3 minutes and 45 seconds.

# Additional Changes
* Fixed issue from A2 where pressing 'List all movies' points to a url with no page number (from A2 testing, this functioned the same as having /list/ in the url)

#References:
* Favicon created using favicon.io https://favicon.io/emoji-favicons/film-projector/
* https://stackoverflow.com/questions/35774060/determine-which-wtforms-button-was-pressed-in-a-flask-view
* https://stackoverflow.com/questions/46761931/integerfield-not-validating-on-empty-string
