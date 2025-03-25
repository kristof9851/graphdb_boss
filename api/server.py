from flask import Flask
from graphdb_boss.api.routes import get_node, get_nodes, get_neighbours


def create(app_name='graphdb_boss_api'):
    app = Flask(app_name)

    app.register_blueprint(get_node.blueprint)
    app.register_blueprint(get_nodes.blueprint)
    app.register_blueprint(get_neighbours.blueprint)

    return app
