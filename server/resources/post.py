from flask_jwt_extended import jwt_required, get_current_user
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from server import db
from server.models import PostModel

_post_parser = RequestParser()
_post_parser.add_argument(
    "body",
    type=str,
    required=True,
    help="User's post text body, this field cannot be blank"
)


class Post(Resource):
    def get(self):
        return {"posts": list(map(lambda post: post.to_json(), PostModel.query.all()))}

    @jwt_required
    def post(self):
        user = get_current_user()
        json_data = _post_parser.parse_args()
        try:
            user.create_post(json_data.get("body"))
            return {"message": f"Post created successfully by {str(user)}"}, 201
        except:
            return {"message": "Something went wrong"}, 500


class PostDetails(Resource):
    def get(self, id):
        return {"post": PostModel.query.get(id).to_json()}

    @jwt_required
    def post(self, id, action):
        current_user = get_current_user()
        post = PostModel.query.get(id)
        if action == "like":
            current_user.like_post(post)
            db.session.commit()
            return {"message": f"Post liked successfully by {str(current_user)}"}, 200
        elif action == "unlike":
            current_user.unlike_post(post)
            db.session.commit()
            return {"message": f"Post unliked successfully by {str(current_user)}"}, 200
        else:
            return {"message": "Something went wrong"}, 500
