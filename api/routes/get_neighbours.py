import json
from flask import jsonify, Blueprint
from mongoengine import DoesNotExist
from graphdb_boss.db.model import Node, Edge


blueprint = Blueprint('get_neighbours', __name__)


# GET /neighbours/<id>
@blueprint.route('/neighbours/<id>', methods=['GET'])
def get_neighbours(id):
    # Find node
    try:
        node = Node.objects.get(id=id)
    except DoesNotExist:
        return jsonify({'error': 'Node not found'}), 404

    # Find all edges where the node is either _from_node or _to_node
    edges = Edge.objects(__raw__={'$or': [
        {'_from_node': node.id}, 
        {'_to_node': node.id}
    ]})

    # Extract the IDs of the neighbouring nodes
    neighbour_ids = set()
    for edge in edges:
        if edge._from_node == node.id or edge._to_node == node.id:
            neighbour_ids.add(node.id)
    
    # Retrieve the neghbouring nodes
    neighbours = Node.objects(id__in=list(neighbour_ids))
    neighbours_map = {n.id: n for n in neighbours}

    # Assemble response
    response = {
        'from': {},
        'to': {}
    }
    for edge in edges:
        if edge._from_node == node.id:
            if edge.name not in response['from']:
                response['from'][edge.name] = []
            
            response['from'][edge.name].append( json.loads(neighbours_map[edge._to_node].to_dict()) )

        if edge._to_node == node.id:
            if edge.name not in response['to']:
                response['to'][edge.name] = []
            
            response['to'][edge.name].append( json.loads(neighbours_map[edge._from_node].to_dict()) )

    return jsonify(response), 200
