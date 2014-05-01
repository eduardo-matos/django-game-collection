## Game Collection

[![Build Status](https://travis-ci.org/eduardo-matos/django-game-collection.png?branch=master)](https://travis-ci.org/eduardo-matos/django-game-collection) [![Coverage Status](https://coveralls.io/repos/eduardo-matos/django-game-collection/badge.png?branch=master)](https://coveralls.io/r/eduardo-matos/django-game-collection?branch=master)

Converting project from [Laravel](https://github.com/eduardo-matos/laravel-game-collection) to Django.

### Installation
Add the following environment variables: `DJANGO_SETTINGS_MODULE` with `game_collection.settings.local` if running locally, or `game_collection.settings.production` if running in production. And `SECRET_KEY` which may be pretty much anything you want, and it will be used by Django itself.

If you're on Linux/Mac, this will do the trick:

```
export DJANGO_SETTINGS_MODULE=game_collection.settings.local
export SECRET_KEY=abc123
```

Remember to choose a hard to remember key on production!

### Running tests
`cd` into `game_collection` directory and run `python ./manage.py test --settings=game_collection.settings.test`. Hopefully everything will be green :v:.
