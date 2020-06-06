import datetime

from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_refresh_token_required, \
    jwt_required, get_raw_jwt
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from server import jwt
from server.models import UserModel, RevokedTokenModel

_user_parser = RequestParser()
_user_parser.add_argument(
    "username",
    type=str,
    required=True,
    help="This field cannot be blank"
)
_user_parser.add_argument(
    "password",
    type=str,
    required=True,
    help="This field cannot be blank"
)


class UserRegistration(Resource):
    def post(self):
        json_data = _user_parser.parse_args()

        if UserModel.find_user_by_username(json_data["username"]):
            return {"message": "User with this username already exists"}, 400

        user = UserModel(**json_data)
        try:
            access_token = create_access_token(identity=json_data['username'])
            refresh_token = create_refresh_token(identity=json_data['username'])

            user.save_to_db(save_time_for="login")
            return {"access_token": access_token,
                    "refresh_token": refresh_token,
                    "message": f"{str(user)} successfully created"}, 201
        except:
            return {"message": "Something went wrong"}, 500


class UserLogin(Resource):
    def post(self):
        json_data = _user_parser.parse_args()
        username = json_data["username"]
        current_user = UserModel.find_user_by_username(username)

        if not current_user:
            return {"message": f"User {username} doesn't exist"}

        if current_user.check_password(json_data["password"]):
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)

            current_user.save_to_db(save_time_for="login")
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }, 200
        else:
            return {"message": "Provided invalid credentials"}, 401


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user_id = get_jwt_identity()
        access_token = create_access_token(identity=current_user_id, fresh=False)
        return {"access_token": access_token}, 200


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    user = UserModel.find_user_by_username(username=identity)

    if not user:
        return None

    user.save_to_db(save_time_for="request")
    return user


@jwt.user_loader_error_loader
def custom_user_loader_error(identity):
    return jsonify({"message": f"User {identity} not found"}), 404


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)
