from flask import Blueprint
from flask_restful import Api

from server.resources.posts import Post
from server.resources.auth import TokenRefresh, UserLogin, UserRegistration, UserLogoutAccess, UserLogoutRefresh

api_bp = Blueprint("api", __name__)
api = Api(api_bp)

api.add_resource(Post, "/posts")

api.add_resource(UserLogin, "/auth/login")
api.add_resource(UserRegistration, "/auth/register")

api.add_resource(UserLogoutAccess, "/logout/access")
api.add_resource(UserLogoutAccess, "/logout/refresh")
