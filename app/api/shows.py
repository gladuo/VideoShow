from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Show
from . import api
from .errors import forbidden


@api.route('/shows/')
def get_shows():
    page = request.args.get('page', 1, type=int)
    pagination = Show.query.paginate(
        page, per_page=current_app.config['SHOWS_PER_PAGE'],
        error_out=False)
    shows = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_shows', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_shows', page=page+1, _external=True)
    return jsonify({
        'shows': [show.to_json() for show in shows],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/shows/<int:id>')
def get_show(id):
    show = Show.query.get_or_404(id)
    return jsonify(show.to_json())


@api.route('/shows/', methods=['POST'])
def new_show():
    show = Show.from_json(request.json)
    show.author = g.current_user
    db.session.add(show)
    db.session.commit()
    return jsonify(show.to_json()), 201, \
        {'Location': url_for('api.get_show', id=show.id, _external=True)}


@api.route('/shows/<int:id>', methods=['PUT'])
def edit_show(id):
    show = Show.query.get_or_404(id)
    if g.current_user != show.author:
        return forbidden('Insufficient permissions')
    show.body = request.json.get('body', show.body)
    db.session.add(show)
    return jsonify(show.to_json())
