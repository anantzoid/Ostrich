from app import webapp
from app.models import *
import re

class WebUtils():
    @staticmethod
    def fetchSearchResults(query, search_type):
        from app.models import Search
        search = Search(query)
        if search_type == 'category':
            results = search.categorySearch()
        elif search_type == 'collection':
            results = search.collectionsSearch()
        else: 
            results = search.basicSearch()
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


