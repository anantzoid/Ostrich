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
    page = Utils.getParam(request.args, 'page', var_type='int', default=1)
    search_type = Utils.getParam(request.args, 'type', default='free')
    user_id = Utils.getParam(request.args, 'userId', 'int')
    flow = Utils.getParam(request.args, 'flow', default='borrow')

    if not query:
        return jsonify(response), webapp.config['HTTP_STATUS_CODE_DATA_MISSING']
    
    search = Search(query, user_id, flow)
    if search_type == 'free':
        results = search.basicSearch(page=page-1)
    elif search_type == 'category':
        results = search.categorySearch(page=page-1)
    elif search_type == 'isbn':
        results = search.isbnSearch(page=page-1)
    elif search_type == 'custom':
        results = search.customQuery()
        return results
    #log
    Search.logSearch({_:request.args.get(_) for _ in request.args})
    return jsonify(results)

@webapp.route('/getCategories')
def getCategories():
    categories = Search.getSearchCategories()
    return json.dumps(categories)

@webapp.route('/searchFail', methods=['POST'])
def searchFail():
    user_id = Utils.getParam(request.form, 'user_id', 'int')
    q = Utils.getParam(request.form, 'q')
    q_type = Utils.getParam(request.form,'type')
    flow = Utils.getParam(request.form, 'flow', default='borrow')
    
    Search(q, user_id, flow).reportFail(q_type)
    return jsonify(status='true')

@webapp.route('/recommended', methods=['GET'])
def recommended():
    return json.dumps(Search([]).mostRecommended())

@webapp.route('/mostSearched', methods=['GET'])
def mostSearched():
    return json.dumps(Search([]).mostSearched())


