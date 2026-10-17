# Flask-SQLAlchemy Serialization Lab

## Description
A small e-commerce backend with Customer, Item and Review models.
Reviews connect customers and items. Customers can reach their items
through an association proxy, and Marshmallow schemas serialize the data
without recursion errors.

## Setup
    pipenv install
    pipenv shell
    cd server
    flask db upgrade head
    python seed.py

## Tests
    pytest

## Screenshot
![Passing tests](server/screenshot.png)