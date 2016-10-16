from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Video
from . import api
from .errors import forbidden


@api.route('/videos/')
def get_videos():
    page = request.args.get('page', 1, type=int)
    pagination = Video.query.paginate(
        page, per_page=current_app.config['VIDEOS_PER_PAGE'],
        error_out=False)
    videos = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_videos', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_videos', page=page+1, _external=True)
    return jsonify({
        'videos': [video.to_json() for video in videos],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/videos/<int:id>')
def get_video(id):
    video = Video.query.get_or_404(id)
    return jsonify(video.to_json())


@api.route('/videos/', methods=['POST'])
def new_video():
    video = Video.from_json(request.json)
    video.author = g.current_user
    db.session.add(video)
    db.session.commit()
    return jsonify(video.to_json()), 201, \
        {'Location': url_for('api.get_post', id=video.id, _external=True)}


@api.route('/videos/<int:id>', methods=['PUT'])
def edit_video(id):
    video = Video.query.get_or_404(id)
    if g.current_user != video.author:
        return forbidden('Insufficient permissions')
    video.body = request.json.get('body', video.body)
    db.session.add(video)
    return jsonify(video.to_json())
