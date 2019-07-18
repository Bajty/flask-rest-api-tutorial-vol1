# flask-rest-api-tutorial-vol1

> Výsledok prvého workshopu Flask REST API s použitím Python Flask, SQL Alchemy a Marshmallow

## Ako začať s Pipenv

``` bash
# Aktivovať venv
$ pipenv shell

# Inštalovať závislosti
$ pipenv install

# Vytvorenie sqlite DB
$ python
>> from app import db
>> db.create_all()
>> exit()

# Vývojový server (http://localhst:5000)
python app.py
```

## Endpoints

* GET     /todo
* GET     /todo/:id
* POST    /todo
* PUT     /todo/:id
* DELETE  /todo/:id
* GET     /user
* POST    /user
