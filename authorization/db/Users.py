import time

from application.db.db import get_db

db_loc = get_db()


class Users(db_loc.Model):
    id = db_loc.Column(db_loc.Integer, primary_key=True)
    username = db_loc.Column(db_loc.String(30), nullable=False)
    password = db_loc.Column(db_loc.String(20), nullable=False)
    last_online = db_loc.Column(db_loc.Date)

    def __init__(self, username, password,
                 last_online=time.strftime('%Y-%m-%d %H:%M:%S')):
        self.username = username
        self.password = password
        self.last_online = last_online

    def __str__(self):
        return f'{type(self).__name__}: Authors = {self.username}, ' \
            f'Title = {self.password}, Key words = {self.last_online}'

    def set_time(self, last_online):
        self.last_online = last_online
