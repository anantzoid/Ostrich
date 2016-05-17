from app import webapp
from app.models import *

class WebUtils():
    @staticmethod
    def fetchSearchResults(query, search_type):
        search = Search(query)
        if search_type == 'category':
            results = search.categorySearch()
        elif search_type == 'collections':
            results = search.collectionsSearch()
        else: 
            results = search.basicSearch()
        results['items'] = WebUtils.extendItemWebProperties(results['items'])
        return results 

    @staticmethod
    def extendItemWebProperties(items):
        for i, item in enumerate(items):
            items[i]['img_small'] = webapp.config['S3_HOST'] + item['img_small'] 
            items[i]['item_url'] = webapp.config['HOST']  + '/book/rent/' + str(item['item_id'])
            # NOTE remove this later. Only for Test environment becuase we're poor
            try:
                if item['slug_url']:
                    items[i]['item_url'] += '-' + item['slug_url']
            except:
                pass
        return items

