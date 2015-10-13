from app import webapp
from app.models import Search 
from flask import request, jsonify


@webapp.route('/search', methods=['GET'])
def search():
    q = request.args.get('q')
    page = int(request.args.get('page')) if 'page' in request.args else 1

    if 'type' in request.args and request.args.get('type') == 'title':
        results = Search.searchQueryByName(q, page) 
    else:
        results = Search.searchQuery(q, page) 

    if len(results) == 1:
        return jsonify(results[0])
    else:
        return jsonify(results=results)
