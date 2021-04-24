"""User REST API."""

from flask_restful import Resource
from application.service import UserService


class UserResource(Resource):
    def get(self, id: int = None):
        if id is not None:
            user = UserService.get_by_id(id)
            return user.as_dict()
        else:
            users = UserService.get_all()
            return [user.as_dict() for user in users]
