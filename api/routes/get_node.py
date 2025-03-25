from flask import jsonify, Blueprint
from graphdb_boss.db.model import Node
from mongoengine import DoesNotExist


blueprint = Blueprint('get_node', __name__)


# GET /nodes/<id>
@blueprint.route('/nodes/<id>', methods=['GET'])
def get_node(id):
    try:
        node = Node.objects.get(id=id)
        return node.to_json(), 200
    except DoesNotExist:
        return jsonify({'error': 'Node not found'}), 404
