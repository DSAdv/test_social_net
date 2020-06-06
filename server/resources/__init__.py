from flask import Blueprint
from flask_restful import Api

from server.resources.posts import Post
from server.resources import auth

api_bp = Blueprint("api", __name__)
api = Api(api_bp)

api.add_resource(Post, "/posts")

api.add_resource(auth.UserLogin, "/auth/login")
api.add_resource(auth.UserRegistration, "/auth/register")

api.add_resource(auth.UserLogoutAccess, "/logout/access")
api.add_resource(auth.UserLogoutRefresh, "/logout/refresh")

api.add_resource(auth.Secret, "/secret")
