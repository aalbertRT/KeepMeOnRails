from pytest import fixture
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from application import create_app

@fixture
def app() -> Flask:
    return create_app(testing=True)

@fixture
def db(app: Flask) -> SQLAlchemy:
    from application import db
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()
        db.session.commit()
