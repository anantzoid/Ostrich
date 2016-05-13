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

        for i, item in enumerate(results['items']):
            results['items'][i]['img_small'] = webapp.config['S3_HOST'] + item['img_small'] 
            results['items'][i]['item_url'] = Item.getItemPageUrl(item)
        return results 

    @staticmethod
    def fetchWebCatalog():
        # NOTE For now
        return Collection.getHomepageCollections(items=True)

