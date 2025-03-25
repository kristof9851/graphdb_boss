import json
from flask import jsonify, Blueprint, request
from graphdb_boss.db.model import Node


blueprint = Blueprint('get_nodes', __name__)


def get_all_keys():
    # Use the aggregation framework to collect all keys
    pipeline = [
        {'$project': {'arrayofkeyvalue': {'$objectToArray': '$$ROOT'}}},
        {'$unwind': '$arrayofkeyvalue'},
        {'$group': {'_id': None, 'allkeys': {'$addToSet': '$arrayofkeyvalue.k'}}}
    ]

    result = Node.objects.aggregate(pipeline)
    keys = next(results, {}).get('allkeys', [])
    return keys

# GET /nodes?filter=<key1:value1,key2:value2,...>&query=<query>&skip=<skip>&limit=<limit>
@blueprint.route('/nodes', methods=['GET'])
def get_nodes():
    # Parse query parameters
    filter_param = request.args.get('filter', '')
    query = request.args.get('query', '')
    skip = int(request.args.get('skip', 0))
    limit = int(request.args.get('limit', 100))

    # Parse filter
    filter_dict = {}
    if len(filter_param) > 0:
        for key_value in filter_param.split(','):
            key, value = key_value.split(':')
            filter_dict[key] = value

    # Get nodes...
    try:
        # Add query filter
        if len(query) > 0:
            fields = get_all_keys()
            or_conditions = [{field: {'$regex': query, '$options': 'i'}} for field in fields]
            filter_dict['$or'] = or_conditions

        # Get nodes
        results = Node.objects(__raw__=filter_dict).skip(skip).limit(limit)
        jsonable_nodes = [json.loads(result.to_json()) for result in results]
        return jsonify(jsonable_nodes), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400