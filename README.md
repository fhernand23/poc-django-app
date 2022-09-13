# Poc-django-app

A complete base app starter in django to customize in a bigger project
Based on DjangoX (https://github.com/wsvincent/djangox)

## Features

- Django 4.0 & Python 3.10
- Install via [Pip](https://pypi.org/project/pip/), [Pipenv](https://pypi.org/project/pipenv/), or [Docker](https://www.docker.com/)
- User log in/out, sign up, password reset via [django-allauth](https://github.com/pennersr/django-allauth)
- Static files configured with [Whitenoise](http://whitenoise.evans.io/en/stable/index.html)
- Styling with [Bootstrap v4](https://github.com/twbs/bootstrap)
- Debugging with [django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar)
- DRY forms with [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms)

## Dev environment

```bash
conda create -n poc-django-app python=3.10
conda activate poc-django-app
```

Install dependencies & modules
```bash
pip install -U -r requirements.txt
```

## Start project

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# Load the site at http://localhost:8000
```

## Clean project
