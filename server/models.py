import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from server import db


class UserModel(db.Model):
    """User account model."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False, unique=False)
    password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False)

    created_on = db.Column(db.DateTime, index=False, unique=False, nullable=True,
                           default=datetime.datetime.utcnow)

    last_login = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    last_request = db.Column(db.DateTime, index=False, unique=False, nullable=True)

    liked = db.relationship("PostLikeModel", foreign_keys="PostLikeModel.user_id", backref="user", lazy="dynamic")
    posts = db.relationship("PostModel", foreign_keys="PostModel.user_id", backref="author", lazy="dynamic")

    def __init__(self, username, password):
        self.username = username
        self.password = None

        self.set_password(password)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def save_to_db(self, save_time_for: str = None):
        if save_time_for is not None:
            if save_time_for.lower() == "login":
                self.last_login = datetime.datetime.utcnow()
            elif save_time_for.lower() == "request":
                self.last_request = datetime.datetime.utcnow()

        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # posts functionality
    def create_post(self, body):
        post = PostModel(body=body, author=self)
        db.session.add(post)
        db.session.commit()

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLikeModel(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLikeModel.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

    def has_liked_post(self, post):
        return PostLikeModel.query.filter(
            PostLikeModel.user_id == self.id,
            PostLikeModel.post_id == post.id).count() > 0

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def to_json(self):
        return {
            "username": self.username,
            "created_on": str(self.created_on),
            "last_login": str(self.last_login),
            "last_request": str(self.last_request),
        }

    @classmethod
    def return_all(cls):
        return {'users': list(map(lambda user: user.to_json(), UserModel.query.all()))}

    @classmethod
    def find_user_by_username(cls, username: str):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_user_by_id(cls, user_id: int):
        return cls.query.filter_by(id=user_id).first()


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)


class PostLikeModel(db.Model):
    __tablename__ = 'post_likes'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)

    @classmethod
    def get_day_count(cls, date):
        filter_date = date.date() if isinstance(date, datetime.datetime) else date
        return len(cls.query.filter(func.date(cls.timestamp) == filter_date).all())


class PostModel(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_json(self):
        return {
            "id": self.id,
            "body": self.body,
            "timestamp": str(self.timestamp),
            "user_id": self.user_id,
            "like_count": len(PostLikeModel.query.filter_by(post_id=self.id).all()),
        }
