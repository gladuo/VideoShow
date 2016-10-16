# coding=utf-8

from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask import current_app, request, url_for
from flask_login import UserMixin

from app.exceptions import ValidationError
from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    avatar_hash = db.Column(db.String(32))
    shows = db.relationship('Show', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    # TODO: Here We Forgery
    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word())
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id, _external=True),
            'username': self.username,
            'email': self.email
        }
        return json_user

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Video(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    shows = db.relationship('Show', backref='show', lazy='dynamic')

    def to_json(self):
        json_video = {
            'url': url_for('api.get_video', id=self.id, _external=True),
            'info': self.info,
            'timestamp': self.timestamp,
            'shows': url_for('api.get_show_comments', id=self.id,
                             _external=True),
            'shows_count': self.shows.count(),
        }
        return json_video


class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'))
    comments = db.relationship('Comment', backref='show', lazy='dynamic')

    # TODO: Here We Forgery
    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        seed()
        user_count = User.query.count()
        # comment_count = Comment.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            # c = Comment.query.offset(randint(0, comment_count - 1)).first()
            s = Show(timestamp=forgery_py.date.date(True),
                     author_id=1,
                     video_id=1)
            db.session.add(s)
            db.session.commit()

    def to_json(self):
        json_show = {
            'url': url_for('api.get_show', id=self.id, _external=True),
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.author_id,
                              _external=True),
            'video_id': self.video_id,
            'comments': url_for('api.get_show_comments', id=self.id,
                                _external=True),
            'comment_count': self.comments.count()
        }
        return json_show

    @staticmethod
    def from_json(json_show):
        body = json_show.get('body')
        if body is None or body == '':
            raise ValidationError('post does not have a body')
        return Show(body=body)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'))

    # TODO: Here We Forgery
    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        for i in range(count):
            c = Comment(body=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
                     timestamp=forgery_py.date.date(True),
                     author_id=1,
                     show_id=1)
            db.session.add(c)
            db.session.commit()

    def to_json(self):
        json_comment = {
            'url': url_for('api.get_comment', id=self.id, _external=True),
            'body': self.body,
            'timestamp': self.timestamp,
            'author': url_for('api.get_user', id=self.author_id, _external=True),
            'show': url_for('api.get_show', id=self.show_id, _external=True)
        }
        return json_comment

    @staticmethod
    def from_json(json_comment):
        body = json_comment.get('body')
        if body is None or body == '':
            raise ValidationError('comment does not have a body')
        return Comment(body=body)
