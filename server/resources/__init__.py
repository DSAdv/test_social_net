from flask import Blueprint
from flask_restful import Api

from server.resources import auth, post, user

api_bp = Blueprint("api", __name__)
api = Api(api_bp)

api.add_resource(post.Post, "/posts")
api.add_resource(post.PostDetails, "/posts/<int:id>", "/posts/<int:id>/<string:action>")

api.add_resource(user.UserList, "/users")
api.add_resource(user.UserActivity, "/users/self")

api.add_resource(auth.UserLogin, "/auth/login")
api.add_resource(auth.UserRegistration, "/auth/register")
api.add_resource(auth.TokenRefresh, "/auth/refresh")

api.add_resource(auth.UserLogoutAccess, "/logout/access")
api.add_resource(auth.UserLogoutRefresh, "/logout/refresh")
