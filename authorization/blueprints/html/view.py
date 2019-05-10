from flask import Blueprint, render_template

html_view = Blueprint('html_view', __name__)


@html_view.route('/', methods=['GET'])
def index():
    return render_template('index.html')
