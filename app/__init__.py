from flask import Flask, request, g
from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy
from config import config


db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    def validate_access_token():
        if request.method != 'OPTIONS' and 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if len(auth_header.split()) > 1:
                token = auth_header.split()[1]
                from app.users.models import User
                g.current_user = User.verify_auth_token(token)

    app.before_request(validate_access_token)

    from .graphql_schema import schema
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True,
        )
    )

    return app
