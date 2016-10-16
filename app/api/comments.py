from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Show, Comment
from . import api


@api.route('/shows/<int:id>/comments/')
def get_show_comments(id):
    show = Show.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = show.comments.order_by(Comment.timestamp.asc()).paginate(
        page=page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_show_comments', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_show_comments', page=page+1, _external=True)
    return jsonify({
        'comments': [comment.to_json() for comment in comments],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/shows/<int:id>/comments/', methods=['POST'])
def new_show_comment(id):
    show = Show.query.get_or_404(id)
    comment = Comment.from_json(request.json)
    comment.author = g.current_user
    comment.post = show
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_json()), 201, \
        {'Location': url_for('api.get_comment', id=comment.id,
                             _external=True)}
