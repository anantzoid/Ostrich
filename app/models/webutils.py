from app import webapp
from app.models import *
from flask import session
import re

class WebUtils():
    @staticmethod
    def storeUserSession(user):
        from app.models import User
        # TODO refresh cache when implemented
        user.getOrderSlots()
        user_obj = user.getObj()
        user_obj['wishlist'] = User.getWishlist(user_obj['user_id'], False)
        session['_user'] = user_obj

    @staticmethod
    def fetchSearchResults(query, search_type, page):
        from app.models import Search

        user_info = {'user_id': -1, 'uuid': 'web:-1', 'gcm_id': None}
        user_data = session.get('_user', None)
        if user_data:
            user_info['user_id'] = user_data['user_id'] 
            user_info['uuid'] = 'web:'+str(user_data['user_id']) 

        search = Search(query, user_info)
        page = page - 1
        if search_type == 'category':
            results = search.categorySearch(page)
        elif search_type == 'collection':
            results = search.collectionsSearch(page)
        else: 
            results = search.basicSearch(page)
        results['items'] = WebUtils.extendItemWebProperties(results['items'])
        return results 

    @staticmethod
    def extendItemWebProperties(items):
        for i, item in enumerate(items):
            items[i]['item_name'] = re.sub("\(.*\)", "", item['item_name']).strip()
            if item['img_small']:
                items[i]['img_small'] = webapp.config['S3_HOST'] + item['img_small'] 
            else:
                items[i]['img_small'] = '/static/img/book_placeholder.png'
            items[i]['item_url'] = webapp.config['HOST']  + '/book/rent/' + str(item['item_id'])
            # NOTE remove this later. Only for Test environment becuase we're poor
            try:
                if item['slug_url']:
                    items[i]['item_url'] += '-' + item['slug_url']
            except:
                pass
        return items

    @staticmethod
    def extendCategoryProperties(category):
        url = webapp.config['HOST']  + '/books/category/'
        if category['slug_url']: 
            category['slug_url'] = url + category['slug_url']
        else:
            category['slug_url'] = url + str(category['category_id'])
        return category


