from flask import Blueprint, render_template, request, redirect, \
    current_app as app
import numpy as np

html_view = Blueprint('html_view', __name__)


@html_view.route('/', methods=['GET'])
def index():
    if 'auth' in request.cookies:
        Amir = '\u0336'
        for c in 'Амир':
            Amir = Amir + c + '\u0336'
        random_int = np.random.random_integers(0, 6)
        aphorisms = ['Это долго, потому что это небыстро. © Амир',
                     '... но в жизни это не так. © Миша',
                     'Можно не парсить - лучше не парсить. © Все',
                     'Я всегда пытаюсь понять, зачем я делаю то, что я делаю. '
                     'Поэтому я на грани депрессии. © Миша',
                     'Человек должен верить, что непонятное можно понять. © '
                     + Amir + ' И. Гётте',
                     'Осталось ещё 5 минут. Но если учитывать, что мы всреднем'
                     ' задерживаем вас на полчаса, то у нас осталось '
                     '35 минут:) © Миша',
                     'Лично мне пригодилось это ровно один раз. © Все']
        user = request.cookies.get('auth')
        app.config['user'] = user
        app.logger.info(app.config['user'] + ' on server')
        app.logger.info(random_int)
        return render_template('index.html', user=user,
                               aphorisms=aphorisms[random_int])
    else:
        return redirect('http://127.0.0.1:5001/')
