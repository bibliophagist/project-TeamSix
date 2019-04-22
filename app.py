from flask import Flask
import logging
from homeworks.homework_06_web.blueprints.main.view import main_view

app = Flask(__name__)
logger = logging.getLogger('app')
app.config['MEMORY'] = []

app.register_blueprint(main_view, url_prefix='/main')


@app.before_first_request
def setup_logging():
    if not app.debug:
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.DEBUG)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8081")
