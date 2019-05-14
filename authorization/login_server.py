from flask import Flask, abort, jsonify, request
import logging
from authorization.blueprints.auth.view import main_view
from authorization.blueprints.html.view import html_view
from flask_bootstrap import Bootstrap

DB_CONFIG = {
    'username': 'team_six_pymail',
    'password': '12345qwe',
    'host': 'www.db4free.net:3306',
    'dbname': 'article_storage',
}

app_login = Flask(__name__)
bootstrap = Bootstrap(app_login)
logger = logging.getLogger('app')
app_login.secret_key = "super secret key"

app_login.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://" \
    f"{DB_CONFIG['username']}:{DB_CONFIG['password']}@" \
    f"{DB_CONFIG['host']}/{DB_CONFIG['dbname']}?charset=utf8"
app_login.config['SQLALCHEMY_ECHO'] = True
app_login.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app_login.config['SQLALCHEMY_RECORD_QUERIES'] = True
app_login.config['MEMORY'] = []

app_login.register_blueprint(main_view, url_prefix='/auth')
app_login.register_blueprint(html_view)


@app_login.before_first_request
def setup_logging():
    if not app_login.debug:
        app_login.logger.addHandler(logging.StreamHandler())
        app_login.logger.setLevel(logging.DEBUG)


if __name__ == "__main__":
    app_login.run(host="127.0.0.1", port="5001")
