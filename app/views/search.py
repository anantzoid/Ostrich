from app import webapp
from app.models import Search , Utils
from flask import request, jsonify
import json


@webapp.route('/search')
def searchString():
    response = {'status': 'False'}

    query = Utils.getParam(request.args, 'q') 
    page = int(Utils.getParam(request.args, 'page', var_type='int', default=1))
    search_type = Utils.getParam(request.args, 'type', default='free')

    if not query:
        return jsonify(response)

    search = Search(query)
    if search_type == 'free':
        results = search.basicSearch(page=page-1)
    elif search_type == 'category':
        results = search.categorySearch(page=page-1)
    elif search_type == 'isbn':
        results = search.isbnSearch(page=page-1)

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


