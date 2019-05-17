import pandas as pd
from flask import Flask
import logging
from application.blueprints.main.view import main_view
from application.blueprints.html.view import html_view
from flask_bootstrap import Bootstrap

from application.db import db

app = Flask(__name__)
bootstrap = Bootstrap(app)
logger = logging.getLogger('app')
app.secret_key = "super secret key"

# DB_CONFIG = {
#     'username': 'team_six_pymail',
#     'password': '12345qwe',
#     'host': 'www.db4free.net:3306',
#     'dbname': 'article_storage',
# }

DB_CONFIG = {
    'username': 'bibliophagist',
    'password': '5264552',
    'host': 'localhost:3306',
    'dbname': 'article_seeker',
}

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://" \
    f"{DB_CONFIG['username']}:{DB_CONFIG['password']}@" \
    f"{DB_CONFIG['host']}/{DB_CONFIG['dbname']}?charset=utf8"
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.config['user'] = None

app.register_blueprint(main_view, url_prefix='/auth')
app.register_blueprint(html_view)


@app.before_first_request
def setup_logging():
    if not app.debug:
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.DEBUG)


def write_data():
    from application.db.Articles import Articles

    data = pd.read_sql(db.get_db().session.query(Articles).statement,
                       app.config['SQLALCHEMY_DATABASE_URI'])
    data.to_csv('article_from_db.csv', index=None)
    from application.machine.Seeker import Seeker
    app.config['seeker'] = Seeker()


@app.before_first_request
def init_machine():
    data = pd.read_csv('article_from_db.csv')
    from application.machine.Seeker import Seeker
    app.config['seeker'] = Seeker(data)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000")
