from app import webapp
from app.models import Search, Order, User, Collection, Utils
from flask import jsonify, request
from app.decorators import async

from pymongo import MongoClient
from app.scripts.related_items import getRelatedItems
import json

@webapp.route('/startSession')
def startSession():
    if 'android_id' in request.args:
        android_id = request.args.get('android_id')
        if android_id in []:
            return jsonify({'debug':'True', 'ip': '52.74.20.228'})

    # VERSION SPECIFIC
    app_version = int(request.headers.get('App-Version')) if 'App-Version' in request.headers else 0
    
    # Search().getContentData(key="recommendations")
    # Search().getContentData(key="most_searched")

    reading_multiplier = webapp.config['NEW_READING_RATE'] if app_version >= 6030000 else webapp.config['NEW_READING_RATE'] - 0.01
    data = {
        'most_searched': Collection(4).getObj()['items'],
        'recommendations': Collection(5).getObj()['items'],
        'categories': Search.getSearchCategoriesForApp(),
        'return_days': webapp.config['DEFAULT_RETURN_DAYS'],
        'reading_multiplier': reading_multiplier,
        'time_slots': Order.getTimeSlotsForOrder(),
        'user_model': None
    }

    if 'user_id' in request.args:
        user_id = request.args.get('user_id')
        if user_id and int(user_id) > -1:
            user = User(user_id)
            user.getOrderSlots()
            data['user_model'] = user.getObj()
            user.logMetadata(app_version)
    return jsonify(data)

@webapp.route('/getRelatedItems')
def getRelatedItemsApi():
    client = MongoClient(webapp.config['MONGO_DB'])
    db = client.ostrich

    item_id = Utils.getParam(request.args, 'item_id', 'int')

    related_items_cursor = db.related_item_ids.find({'_id': item_id})
    related_item_ids = [_ for _ in related_items_cursor]

    if len(related_item_ids) == 0:
        #check redis queue
        getRelatedItemsAsyncWrapper(item_id)
        return jsonify({'status': 'wait', 'message':'Crawling in progress'})

    related_item_ids = related_item_ids[0]['item_ids']
    items = Search().getById(related_item_ids)
    return json.dumps(items)

@async
def getRelatedItemsAsyncWrapper(item_id):
    getRelatedItems(item_id)
    return
