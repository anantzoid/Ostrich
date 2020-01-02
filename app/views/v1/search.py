from app import webapp, mysql
from app.models import Search , Utils, Collection, WebUtils
from flask import request, jsonify
from flask.ext.jsonpify import jsonify as jsonp
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
    results = {}

    query = Utils.getParam(request.args, 'q') 
    page = Utils.getParam(request.args, 'page', var_type='int', default=1)
    search_type = Utils.getParam(request.args, 'type', default='free')
    user_id = Utils.getParam(request.args, 'userId', 'int')
    flow = Utils.getParam(request.args, 'flow', default='borrow')
    gcm_id = Utils.getParam(request.args, 'gcm_id', default=None)
    uuid = Utils.getParam(request.args, 'distinct_id', default=None)
    ref = Utils.getParam(request.args, 'ref', default='mobile')

    if not query:
        return Utils.errorResponse(response, 'HTTP_STATUS_CODE_DATA_MISSING')
   
    if ref == 'web':
        return jsonify(WebUtils.fetchSearchResults(query, search_type, page))

    user_info = {'user_id': user_id, 'gcm_id': gcm_id, 'uuid': uuid}
    search = Search(query, user_info, flow)
    if search_type == 'free':
        results = search.basicSearch(page=page-1)
    elif search_type == 'category':
        results = search.categorySearch(page=page-1)
    elif search_type == 'collections':
        results = search.collectionsSearch(page=page-1)
    elif search_type == 'isbn':
        results = search.isbnSearch(page=page-1)
    elif search_type == 'auto':
        results = search.autoComplete()
    elif search_type == 'custom':
        results = search.customQuery()
        return results
    #log
    if user_id not in Utils.getAdmins():
        Search.logSearch({_:request.args.get(_) for _ in request.args}, search_type)

    return jsonify(results) if flow != 'admin' else jsonp(results)

@webapp.route('/getCategories')
def getCategories():
    categories = Search.getSearchCategoriesForApp()
    return jsonify(categories)

@webapp.route('/getCollectionCategory')
def getCollectionCategory():
   return jsonify(Collection.getByCategory())

@webapp.route('/searchFail', methods=['POST'])
def searchFail():
    #NOTE deprecated. Done directly from backend
    return jsonify(status='true')
    
    user_id = Utils.getParam(request.form, 'user_id', 'int')
    q = Utils.getParam(request.form, 'q')
    q_type = Utils.getParam(request.form,'type')
    flow = Utils.getParam(request.form, 'flow', default='borrow')
    
    Search(q, {'user_id': user_id}, flow).reportFail(True,True,q_type)
    return jsonify(status='true')

@webapp.route('/recommended', methods=['GET'])
def recommended():
    return jsonify(Search([]).mostRecommended())

@webapp.route('/mostSearched', methods=['GET'])
def mostSearched():
    return jsonify(Search([]).mostSearched())

@webapp.route('/getMultiplePanels')
def getMultiplePanels():
    cursor = mysql.connect().cursor()
    cursor.execute("""SELECT collection_id FROM collections WHERE active = 1 AND
        partial_order = 1 ORDER BY collection_id DESC""")
    panels = []
    for col_id in cursor.fetchall():
        panels.append(Collection(col_id).getObj())
    return jsonify(panels)

