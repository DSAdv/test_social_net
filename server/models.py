import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from server import db


class UserModel(db.Model):
    """User account model."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False, unique=False)
    password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False)

    created_on = db.Column(db.DateTime, index=False, unique=False, nullable=True,
                           default=datetime.datetime.now)

    last_login = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    last_request = db.Column(db.DateTime, index=False, unique=False, nullable=True)

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
            {
                "login": self.last_login,
                "request": self.last_request,
            }[save_time_for] = datetime.datetime.now()

        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<User {}>'.format(self.username)

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
