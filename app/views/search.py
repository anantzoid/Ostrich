from app import webapp
from app.models import Search , Utils
from flask import request, jsonify
import json


'''
    Generic search call
    @params
        q: search query
        page: the page number of search results (default 0)
        type: type of search: {default: free(all fields), category, isbn}

    @response
        List of search result objects(ES)
'''
@webapp.route('/search')
def searchString():
    response = {'status': 'False'}

    query = Utils.getParam(request.args, 'q') 
    page = int(Utils.getParam(request.args, 'page', var_type='int', default=1))
    search_type = Utils.getParam(request.args, 'type', default='free')

    if not query:
        return jsonify(response), webapp.config['HTTP_STATUS_CODE_DATA_MISSING']

    search = Search(query)
    if search_type == 'free':
        results = search.basicSearch(page=page-1)
    elif search_type == 'category':
        results = search.categorySearch(page=page-1)
    elif search_type == 'isbn':
        results = search.isbnSearch(page=page-1)
    elif search_type == 'custom':
        results = search.customQuery()
        return results

    return jsonify(results)

@webapp.route('/getCategories')
def getCategories():
    categories = Search.getSearchCategories()
    return jsonify(categories=categories)

@webapp.route('/searchFail', methods=['GET'])
def searchFail():
    user_id = Utils.getParam(request.args, 'user_id', 'int')
    q = Utils.getParam(request.args, 'q')
    q_type = Utils.getParam(request.args,'type')
    
    Search.reportFail(user_id, q, q_type)
    return jsonify(status='true')

#@webapp.route('/recommended', methods=['GET'])

