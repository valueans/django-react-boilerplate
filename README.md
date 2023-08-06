# [Kapoor Software Solutions](https://kapoorsoftware.com)


kapoorsoftwaresolutions

License: MIT

## How to start this project

### using virtualenv
1. pip install virtualenv
2. virtualenv venv
3. source venv/bin/activate (on linux and mac)
4. source venv/Script/activate (on windows)
5. pip install -r requirement/base.txt
6. pip install -r requirement/local.txt

### using docker
1. cd kapoor_software
2. docker-compose -f local.yml up --build -d
3. docker-compose -f local.yml run --rm django
if you want to create a superuser you can run 
4. docker-compose -f local.yml run --rm django python manage.py createsuperuser

## Basic Commands

### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

-   To create a **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy kapoor_software

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

### Celery

This app comes with Celery.

To run a celery worker:

``` bash
cd kapoor_software
celery -A config.celery_app worker -l info
```

To run a celery  beat:

``` bash
cd kapoor_software
celery -A config.celery_app beat -l info
```

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.


### Docker
