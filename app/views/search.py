from app import webapp
from app.models import Item 
from flask import request, jsonify


@webapp.route('/search', methods=['GET'])
def search():
    q = request.args.get('q')
    results = Item.searchQuery(q) 
    return jsonify(results)
