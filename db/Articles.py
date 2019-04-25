from flask import Flask, g, current_app as app
from db.db import get_db

db_loc = get_db()


class Articles(db_loc.Model):
    id = db_loc.Column(db_loc.Integer, primary_key=True)
    title = db_loc.Column(db_loc.String(200), nullable=False)
    authors = db_loc.Column(db_loc.String(100), nullable=False)
    key_words = db_loc.Column(db_loc.String(200), nullable=False)
    annotation = db_loc.Column(db_loc.Text)

    def __init__(self, title, authors, key_words, annotation):
        self.title = title
        self.authors = authors
        self.key_words = key_words
        self.annotation = annotation

    def __str__(self):
        return f'{type(self).__name__}: Authors = {self.authors}, ' \
            f'Title = {self.title}, Key words = {self.key_words}, ' \
            f'Annotation = {self.annotation}'
