from app import webapp
from app.models import *
from flask import request, jsonify
import json

@webapp.route('/submitReview', methods=['POST'])
def submitReview():
    response = {'status': 'False'}
    
    review_id = Review.submitReview(request.form)
    if review_id:
        review = Review(review_id).getObj()
        return jsonify(review)
    else:
        return Utils.errorResponse(response)

@webapp.route('/editReview', methods=['POST'])
def editReview():
    review_id = Utils.getParam(request.form, 'review_id', 'int')
    review = Review(review_id) 
    review.editReview(request.form)
    review = Review(review_id).getObj()
    return jsonify(review)
