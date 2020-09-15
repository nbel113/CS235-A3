# CompSci 235 A2 - CS235Flix - nbel113

## Description
Nigel Bell's submission for CompSci 235's Assignment 2, based on the course's skeleton python project CS235Flix.

* This web application demonstrates the use of Python's Flask framework. 
* It makes use of libraries such as the Jinja templating library and WTForms. 
* Architectural design patterns and principles including Repository, Dependency Inversion and Single Responsibility have been used to design the application. 
* This also uses Flask Blueprints to maintain a separation of concerns between application functions. 
* Testing includes unit and end-to-end testing using the pytest tool. 

## Installation

**Installation via requirements.txt**

```shell
$ cd CS235-A2
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

Testing requires that file *CS235-A2/tests/conftest.py* be edited to set the value of `TEST_DATA_PATH`. You should set this to the absolute path of the *CS235-A2/tests/data* directory. 
Run testing with:
```
python -m pytest
```
E.g. 

`TEST_DATA_PATH = os.path.join('C:', os.sep, 'Users', 'ian', 'Documents', 'Python dev', 'COVID-19', 'tests', 'data')`

assigns TEST_DATA_PATH with the following value (the use of os.path.join and os.sep ensures use of the correct platform path separator):

`C:\Users\ian\Documents\python-dev\COVID-19\tests\data`

You can then run tests from within PyCharm.



