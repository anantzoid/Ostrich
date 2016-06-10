from app import webapp
from flask import request, jsonify, render_template, Response
import json
import requests
from app.models import *
import re
from pymongo import MongoClient
from app.decorators import async

ssl_link = 'https://4c53d7b9.ngrok.io'

@async
def logAuthDetails(auth_details):
    client =  MongoClient(webapp.config['MONGO_DB'])
    db = client.ostrich
    db.slack_auth.update_one({'_id': auth_details['team_id']}, {'$set': auth_details}, upsert=True)
    return

@async
def placeOrder(request, user_data):
    client =  MongoClient(webapp.config['MONGO_DB'])
    db = client.ostrich
    access_token = ''
    for record in db.slack_auth.find({'_id':request['team_id']}):
        access_token = record['access_token']
    data = {
            'token': access_token,
            'user': request['user_id']
            }
    user_info = requests.post('https://slack.com/api/users.info', data=data)
    if user_info.status_code == 200:
        user_info = json.loads(user_info.text)
        if user_info['ok']:
           user_data["email"] = user_info["user"]["profile"]["email"]
    User.b2bUser(user_data)
    return

@webapp.route('/slackapp')
def slackIndex():
    return render_template('slackpage.html', ssl_link=ssl_link)

@webapp.route('/oauth')
def oauth():
    payload = {
            'client_id': '4256151918.31600537060',
            'client_secret': 'fe9d1bb5da50e778756384966a863dce',
            'code': request.args.get('code'),
            'redirect_uri': ssl_link + '/oauth'
            }
    req = requests.get('https://slack.com/api/oauth.access', params=payload)
    response = json.loads(req.text)
    logAuthDetails(response) 
    return jsonify(response)

@webapp.route('/slack/search', methods=['POST'])
def searchbook():
    query = request.form['text']
    if not query:
        return "Sorry, didn't get your query. Please enter /search <query>"

    search = Search(query, {}, 'slack_borrow')
    results = search.basicSearch()
    search_results = []
    for result in results['items']:
        search_results.append("*"+str(result['item_id'])+"*: _"+result['item_name']+"_")
    response = { 
            "username": "Ostrich",
            "text": "\n".join(search_results),
            "mrkdwn": True
            }
    return Response(json.dumps(response),  mimetype='application/json')
    
@webapp.route('/slack/view', methods=['POST'])
def viewbook():
    book_id = request.form['text']
    if (not book_id) or (book_id and not book_id.isdigit()):
        return "Please enter a valid book_id"

    results = Search().getById([int(book_id)])
    if results:
        results = results[0]
    response = {
            "text": "_Book Details_",
            "attachments": [{
                "fallback": results['item_name']+": "+results['author'],
                "color": "#36a64f",
                "title": results['item_name'],
                "text": results['author'],
                "fields": [
                    {
                        "title": "Ratings",
                        "value": results['ratings'],
                        "short": True
                    },
                    {
                        "title": "Charge for 21 days",
                        "value":  'Rs. '+str(results['custom_price']) if 'custom_price' in results else 'Rs. 45',
                        "short": True
                    },
                    {
                        "title": "Genres",
                        "value": ", ".join(results['categories']),
                        "short": False
                    }
                    ],
                "thumb_url": webapp.config['S3_HOST']+results['img_small'] 
                }]
            }
    return Response(json.dumps(response),  mimetype='application/json')

@webapp.route('/slack/rent', methods=['POST'])
def rentbook():
    from app import cache
    data = request.form['text']
    if not data:
        return "Please enter book_id and locality after /rent"

    print request.form
    cache.set(request.form['user_id']+'_book_id', data.split(' ')[0], timeout=10000)
    area = ' '.join(data.split(' ')[1:])
    validation = User.validateLocality(area)
    if validation['is_valid']:
        response = {
                "username": "Ostrich",
                "mrkdwn": True,
                "text": "*"+validation['delivery_message']+"*\n Please enter /contact full_address phone_number. Eg.: /contact 58,1st Main Road 9898989898"
                }
        return Response(json.dumps(response),  mimetype='application/json')
    else:
        return validation['delivery_message']+": Sorry. Ostrich doesn't deliver here yet :slightly_frowning_face:"

@webapp.route('/slack/contact', methods=['POST'])
def contact():
    from app import cache
    contact = request.form['text']
    if not contact:
        return "Please enter address and phone after /contact"

    book_id = cache.get(request.form['user_id']+'_book_id')
    if not book_id:
        return "Please initiate the rent process first using /rent command"

    group = re.search('\d+$', contact)
    if group:
        phone = group.group(0)
        if len(phone) != 10:
            return "Please enter a 10 digit phone number after address"
        address = contact.replace(phone, '')
        if not address:
            return "Please enter your address"
    else:
        return "Please enter a 10 digit phone number after address"
    
    user_data = {
            'email': '',
            'phone': phone,
            'address': address,
            'book_id': book_id,
            'org': request.form['team_domain']
            }
    placeOrder(request.form, user_data)
    return "Placing your order now :grinning:. Download me from <https://play.google.com/store/apps/details?id=in.hasslefree.ostrichbooks&hl=en|play store> to track your order status"


