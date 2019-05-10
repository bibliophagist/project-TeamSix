#!/usr/bin/env python
# coding: utf-8
from flask import request, Blueprint, abort, current_app as app
from application.request.request import Request
from application.request.request_type import RequestType
from sqlalchemy.sql.expression import func
from application.db import db

main_view = Blueprint('main_view', __name__)


@main_view.route("/random_paper", methods=['GET'])
def random_paper():
    name = "Get random paper request"
    app.logger.info(name)

    our_request = Request(RequestType.GET_RANDOM_PAPER)
    app.config['MEMORY'].append(our_request)

    from application.db.Articles import Articles
    article = db.get_db().session.query(Articles).order_by(
        func.random()).first()

    return str(article)


@main_view.route("/get_paper", methods=['GET'])
def get_paper():
    name = "Get paper request"
    app.logger.info(name)
    title = request.args.get('Title')
    if not title:
        app.logger.debug('Parameter incorrect for %s', name)
        return abort(400)

    our_request = Request(RequestType.GET_PAPER, title=title)
    app.config['MEMORY'].append(our_request)

    from application.db.Articles import Articles
    article = db.get_db().session.query(Articles).filter_by(
        title=our_request.title).first()
    return str(article)


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
                          data.get('Annotation'))
    if not (
            our_request.authors and our_request.title and our_request.key_words
            and our_request.annotation):
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
                          data.get('Annotation'), data.get('Ref'))
    if not (
            our_request.authors and our_request.title and our_request.key_words
            and our_request.annotation):
        app.logger.debug('Arguments incorrect for %s', name)
        return abort(400)
    app.config['MEMORY'].append(our_request)

    from application.db.Articles import Articles
    if not db.get_db().session.query(Articles).filter_by(
            title=our_request.title).first():
        articles = Articles(our_request.title, our_request.authors,
                            our_request.key_words, our_request.annotation,
                            our_request.ref)
        db.get_db().session.add(articles)
        db.get_db().session.commit()
        response = 'was handled successfully'
    else:
        response = 'was handled unsuccessfully: Such article already exists'

    return name + ' ' + response


@main_view.route("/update_paper", methods=['POST'])
def update_paper():
    name = 'Update paper to DB request'
    app.logger.info(name)
    data = request.json
    if not data:
        app.logger.debug('Arguments incorrect for %s', name)
        return abort(400)
    our_request = Request(RequestType.ADD_PAPER, data.get('Authors'),
                          data.get('Title'), data.get('Key words'),
                          data.get('Annotation'), data.get('Ref'))
    if not (
            our_request.authors and our_request.title and our_request.key_words
            and our_request.annotation):
        app.logger.debug('Arguments incorrect for %s', name)
        return abort(400)
    app.config['MEMORY'].append(our_request)

    from application.db.Articles import Articles
    db.get_db().session.query(Articles).filter(
        Articles.title == our_request.title).update(
        {'annotation': our_request.annotation, 'authors': our_request.authors,
         'key_words': our_request.key_words, 'ref': our_request.ref})
    db.get_db().session.commit()

    response = 'was handled successfully'

    return name + ' ' + response


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

    from application.db.Articles import Articles
    article = db.get_db().session.query(Articles).filter_by(
        title=title).first()
    db.get_db().session.delete(article)
    db.get_db().session.commit()

    return '', 204


# TODO for HW 7 task, will delete later
@main_view.route("/rows_number", methods=['GET'])
def rows_number():
    from application.db.Articles import Articles
    rows = db.get_db().session.query(func.count(Articles.id)).scalar()

    return str(rows)
