from app import webapp
from app.models import Search 
from flask import request, jsonify
import json


@webapp.route('/search', methods=['GET'])
def search():
    q = request.args.get('q')
    page = int(request.args.get('page')) if 'page' in request.args else 1

    if 'type' in request.args:
        qtype = request.args.get('type')
        results = Search.searchQueryByType(q, qtype, page) 
    else:
        results = Search.searchQuery(q, page) 

    if len(results) == 1:
        return jsonify(results[0])
    else:
        return json.dumps(results)
