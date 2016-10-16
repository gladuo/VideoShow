from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User, Show


@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/users/<int:id>/shows')
def get_user_shows(id):
    page = request.args.get('page', 1, type=int)
    pagination = Show.query.filter_by(author_id=id).order_by(Show.timestamp.desc()).paginate(
        page, per_page=current_app.config['SHOWS_PER_PAGE'],
        error_out=False)
    shows = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_shows', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_shows', page=page+1, _external=True)
    return jsonify({
        'shows': [show.to_json() for show in shows],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })
