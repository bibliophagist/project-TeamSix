#!/usr/bin/env python
# coding: utf-8
from flask import request, Blueprint, abort, current_app as app
from request.request import Request
from request.request_type import RequestType
from db import db

main_view = Blueprint('main_view', __name__)


@main_view.route("/random_paper", methods=['GET'])
def random_paper():
    name = "Get random paper request"
    app.logger.info(name)
    title = request.args.get('Title')
    if not title:
        app.logger.debug('Parameter incorrect for %s', name)
        return abort(400)

    our_request = Request(RequestType.GET_RANDOM_PAPER)
    app.config['MEMORY'].append(our_request)

    from db.Articles import Articles
    article = Articles.query.get(1)

    # TODO implement request handler

    return article.name


@main_view.route("/find_paper", methods=['POST'])
def find_similar_paper():
    name = 'Find similar paper request'
    app.logger.info(name)
    data = request.json
    if not data:
        app.logger.debug('Arguments incorrect for %s', name)
        return abort(400)
    our_request = Request(RequestType.FIND_SIMILAR_PAPER, data.get('Authors'),
                          data.get('Title'), data.get('Key words'),
                          data.get('Abstract'))
    if not (
            our_request.authors and our_request.title and our_request.key_words
            and our_request.abstract):
        app.logger.debug('Arguments incorrect for %s', name)
        return abort(400)
    app.config['MEMORY'].append(our_request)

    # TODO implement request handler
    response = 'Some response from handler to request'

    return name + ':' + response


@main_view.route("/add_paper", methods=['PATCH'])
def add_paper():
    name = 'Add paper to DB request'
    app.logger.info(name)
    data = request.json
    if not data:
        app.logger.debug('Arguments incorrect for %s', name)
        return abort(400)
    our_request = Request(RequestType.ADD_PAPER, data.get('Authors'),
                          data.get('Title'), data.get('Key words'),
                          data.get('Abstract'))
    if not (
            our_request.authors and our_request.title and our_request.key_words
            and our_request.abstract):
        app.logger.debug('Arguments incorrect for %s', name)
        return abort(400)
    app.config['MEMORY'].append(our_request)

    from db.Articles import Articles
    articles = Articles(our_request.title, our_request.authors,
                        our_request.key_words, our_request.abstract)
    db.get_db().session.add(articles)
    db.get_db().session.commit()

    # TODO implement request handler
    response = 'Some response from handler to request'

    return name + ':' + response


@main_view.route("/delete_paper", methods=['DELETE'])
def delete_paper():
    name = 'Delete paper from DB request'
    app.logger.info(name)
    title = request.args.get('Title')
    if not title:
        app.logger.debug('Parameter incorrect for %s', name)
        return abort(400)

    our_request = Request(RequestType.DELETE_PAPER)
    app.config['MEMORY'].append(our_request)

    from db.Articles import Articles
    article = Articles.query.filter_by(name=title).first()
    db.get_db().session.delete(article)
    db.get_db().session.commit()

    # TODO implement request handler

    return '', 204
