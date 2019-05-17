import time

from application.db.db import get_db

db_loc = get_db()


class History(db_loc.Model):
    id = db_loc.Column(db_loc.Integer, primary_key=True)
    username = db_loc.Column(db_loc.String(30), nullable=False)
    request = db_loc.Column(db_loc.Text, nullable=False)
    response = db_loc.Column(db_loc.Text, nullable=False)
    date = db_loc.Column(db_loc.Date, nullable=False)

    def __init__(self, username, request, response,
                 date=time.strftime('%Y-%m-%d %H:%M:%S')):
        self.date = date
        self.response = response
        self.username = username
        self.request = request

    def __str__(self):
        return f'{type(self).__name__}: Username = {self.username}, ' \
            f'Request = {self.request}, Response = {self.response}'
