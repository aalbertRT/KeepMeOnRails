"""Resources routes module."""

import flask_restful
from application.blueprints.resources.user import UserResource


def initialize_api_routes(api: flask_restful.Api):
    api.add_resource(UserResource, "/users", "/users/<int:id>")
