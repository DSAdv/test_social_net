from flask_restful import Resource

from server.models import UserModel


class UserList(Resource):
    def get(self):
        return UserModel.return_all()
