from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy


def get_db():
    if 'db' not in g:
        g.db = SQLAlchemy(current_app)
    return g.db


def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()
