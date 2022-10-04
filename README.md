# Poc-django-app

A complete base app starter in django to customize in a bigger project
Based on DjangoX (https://github.com/wsvincent/djangox)

## Features

- Django 4.0 & Python 3.10
- Install via [Pip](https://pypi.org/project/pip/) or [Docker](https://www.docker.com/)
- User log in/out, sign up, password reset via [django-allauth](https://github.com/pennersr/django-allauth)
- Static files configured with [Whitenoise](http://whitenoise.evans.io/en/stable/index.html)
- Styling with AdminKit (Bootstrap v5 based template) 
- Debugging with [django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar)
- DRY forms with [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms)

## Dev environment

```bash
python3.9 -m venv venv
. ./venv/bin/activate
pip install -U -r requirements.txt
```

## Start project

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# Load the site at http://localhost:8000
```

dev admin: super1 / 123

## Clean project

- delete db.sqlite3
- delete **/migrations/XXXX_something.py
- run makemigrations
- run migrate
- run createsuperuser
- run server
