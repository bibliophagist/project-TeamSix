from flask import Blueprint, render_template, request, redirect, \
    current_app as app

html_view = Blueprint('html_view', __name__)


@html_view.route('/', methods=['GET'])
def index():
    if 'auth' in request.cookies:
        user = request.cookies.get('auth')
        return render_template('index.html', user=user)
    else:
        return redirect('http://127.0.0.1:5001/')
