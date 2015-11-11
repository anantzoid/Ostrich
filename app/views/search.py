from app import webapp
from app.models import Search , Utils
from flask import request, jsonify
import json


@webapp.route('/search')
def searchString():
    response = {'status': 'False'}

    query = Utils.getParam(request.args, 'q') 
    page = int(Utils.getParam(request.args, 'page', var_type='int', default=1))

    if not query:
        return jsonify(response)

    search = Search(query)
    results = search.basicSearch(page=page-1)
    return jsonify(results=results)


@webapp.route('/sqlsearch', methods=['GET'])
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


