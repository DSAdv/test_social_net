from flask_jwt_extended import jwt_required, get_jwt_identity, get_current_user
from flask_restful import Resource

from server.models import UserModel


class UserActivity(Resource):
    @jwt_required
    def get(self):
        return get_current_user().to_json()


class UserList(Resource):
    def get(self):
        return UserModel.return_all()
