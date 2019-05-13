from flask import Flask
import logging
from application.blueprints.main.view import main_view
from application.blueprints.html.view import html_view

app = Flask(__name__)
logger = logging.getLogger('app')

DB_CONFIG = {
    'username': 'team_six_pymail',
    'password': '12345qwe',
    'host': 'www.db4free.net:3306',
    'dbname': 'article_storage',
}
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://" \
    f"{DB_CONFIG['username']}:{DB_CONFIG['password']}@" \
    f"{DB_CONFIG['host']}/{DB_CONFIG['dbname']}?charset=utf8"
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.config['MEMORY'] = []

app.register_blueprint(main_view, url_prefix='/auth')
app.register_blueprint(html_view)


@app.before_first_request
def setup_logging():
    if not app.debug:
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.DEBUG)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000")
