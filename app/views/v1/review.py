from app import webapp
from app.models import *
from flask import request, jsonify
import json

@webapp.route('/submitReview', methods=['POST'])
def submitReview():
    response = {'status': 'False'}
    
    review_data = json.loads(Utils.getParam(request.form, 'review'))
    review_id = Review.submitReview(review_data)
    if review_id:
        review = Review(review_id).getObj()
        return jsonify(review)
    else:
        return Utils.errorResponse(response)

@webapp.route('/editReview', methods=['POST'])
def editReview():
    review_data = json.loads(Utils.getParam(request.form, 'review'))
    review = Review(review_data['review_id']) 
    review.editReview(review_data)
    review = Review(review_data['review_id']).getObj()
    return jsonify(review)
