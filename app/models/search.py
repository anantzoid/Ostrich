from app import mysql, webapp
from app.models import *
from app.decorators import async
from elasticsearch import Elasticsearch
from pymongo import MongoClient
from datetime import datetime
import requests
import string

class Search():
    def __init__(self, query='', user_info={}, flow='borrow', size=24):
        self.es_url  = webapp.config['ES_NODES'].split(',')
        # NOTE removed ES global object & placed it in individual fns.
        # self.es = Elasticsearch(self.es_url)
        self.query = query
        self.index = 'items_alias'
        self.size = size
        self.flow = flow
        self.search_query = {
                "query": {
                    "function_score": {
                        "query": "",
                        "functions": [
                            {
                                "field_value_factor": {
                                    "field": "num_ratings_int",
                                    "modifier":"sqrt"
                                    }
                                },
                            {
                                "filter":{"term":{"in_stock":1}},
                                "field_value_factor": {
                                    "field": "in_stock",
                                    "factor": 1.2
                                    }
                                }
                            ]
                        }
                    }
                }
        try:
            self.user_id = user_info['user_id'] if user_info['user_id'] else 0
            self.uuid = user_info['uuid']
            self.gcm_id = user_info['gcm_id']
        except:
            pass
        self.str_util = lambda x: ",".join([str(_) for _ in x])


    def basicSearch(self, page=0, source='app'):
        phrase_fail = False 
        query_fail = False

        phrase_results = self.matchPhrase(page)

        if len(phrase_results['items']) == 0:
            phrase_fail = True
        if source == 'app':
            condition = len(phrase_results['items']) in range(11) and len(phrase_results['items']) != 1
        else:
            condition = True
        if condition:
            filter_ids = [_['item_id'] for _ in phrase_results['items']]
            queried_results = self.queryMatch(page, filter_ids)

            if phrase_fail and len(queried_results['items']) == 0 :
                query_fail = True
            phrase_results['items'].extend(queried_results['items'])
            phrase_results['total'] += queried_results['total']
      
        # phrase_results['collections'] = self.getCollectionsFromResults(phrase_results['items'])
        self.reportFail(phrase_fail, query_fail)
        return phrase_results

    def matchPhrase(self, page):
        return self.fetchResultsFromMYSQL(page, " AND i.item_name LIKE '%s%%'"%(self.query))

        data = self.search_query 
        data["query"]["function_score"]["query"] = {"match_phrase": {"item_name": self.query}} 
        return self.executeSearch(data, page)

    def queryMatch(self, page, filter_ids):
        return self.fetchResultsFromMYSQL(page, " AND (i.item_name LIKE '%"+self.query+"%' OR i.author LIKE '%"+self.query+"%')")

        data = self.search_query 
        data["query"]["function_score"]["query"] = {"filtered": {
                            "query": {"query_string": {"query": self.query}},
                            "filter": {"bool": {"must_not":{"ids":{"values": filter_ids}}}}
                        }}
        return self.executeSearch(data, page)

    '''
        Similar to IndexItems. Switching from ES to MySQL
    '''
    def fetchResultsFromMYSQL(self, page, query_condition):
        search_query = """SELECT i.item_id, i.item_name, i.author, i.price,i.ratings, 
        i.num_ratings, i.num_reviews, i.img_small, i.asin, i.goodreads_id, i.summary, i.slug_url,
        (select group_concat(c.category_name SEPARATOR '|') FROM categories c 
        INNER JOIN items_categories ic ON ic.category_id = c.category_id WHERE 
        ic.item_id = i.item_id) AS categories
        FROM items i WHERE i.active=1"""

        if query_condition:
            search_query += " " + query_condition

        page += 1 
        limit = page * self.size
        offset = (page-1) * self.size
        search_query += ' LIMIT %d OFFSET %d'%(limit, offset)

        cursor = mysql.connect().cursor()
        cursor.execute(search_query)

        results = {'items': []}
        num_items = cursor.rowcount
        for num in range(num_items):
            item = Utils.fetchOneAssoc(cursor)
            if item['categories'] is not None:
                item['categories'] = item['categories'].split("|")
            else:
                item['categories'] = []

            item['isbn_10'] = []
            item['isbn_13'] = []
            item['in_stock'] = 0
            item['in_collections'] = []
            item['num_ratings_int'] = 0
            item['num_reviews_int'] = 0

            from app.models import Item
            item.update(Item.getCustomProperties([item]))
            if Item.checkStock(item['item_id']):
                item['in_stock'] = 1

            if item['num_ratings']:
                item['num_ratings_int'] = int(item['num_ratings'].replace(',',''))

            if item['num_reviews']:
                item['num_reviews_int'] = int(item['num_reviews'].replace(',',''))

            results['items'].append(item)
        results['total'] = len(results['items'])
        return results

    def categorySearch(self, page=0):
        cat_search_query = """ and i.item_id in (select icc.item_id from 
        items_categories icc INNER JOIN categories cc on 
        cc.category_id=icc.category_id where cc.category_name='%s')"""%self.query
        return self.fetchResultsFromMYSQL(page,cat_search_query)  

        data = self.search_query 
        data["query"]["function_score"]["query"] = {"match": {"categories": self.query}} 
        return self.executeSearch(data, page)

    def collectionsSearch(self, page=0):
        return {"total":0, "items":[]}

        data = self.search_query 
        data["query"]["function_score"]["query"] = {"match_phrase": {"in_collections": self.query}} 
        return self.executeSearch(data, page)

    def isbnSearch(self, page=0):
        return {"total":0, "items":[]}

        data = self.search_query 
        data["query"]["function_score"]["query"] = {
                "multi_match": {
                    "query": self.query,
                    "fields": ["isbn_10", "isbn_13"]
                    }
                } 
        results = self.executeSearch(data, page)
        if not results['items']:
            self.reportFail(True, True, 'isbn')
        return results

    def getCollectionsFromResults(self, results):
        collections = []
        collection_objects = []
        for result in results:
            if 'in_collections' in result:
                collections.extend(result['in_collections'])
        for collection in list(set(collections)):
            collection_objects.append(self.fetchCollectionObject(collection))
        return collection_objects
        
    def fetchCollectionObject(self, collection_name):
        query = {
                "query": {
                    "match": { "name": collection_name }
                    }
                }
        collection_object = {}
        collection_results = self.executeSearch(query)
        if collection_results['total'] and 'item_ids' in collection_results['items'][0]:
            collection_object = collection_results['items'][0]
            collection_object['items'] = self.getById(collection_object['item_ids']) 
        return collection_object
      
    # NOTE this is not used, so ignored for switching to MySQL
    def autoComplete(self, page=0):
        if len(self.query) < 4:
            return {"items": []}
        data = self.search_query
        data["query"]["function_score"]["query"] = {"match_phrase_prefix":{"item_name":self.query}}
        return self.executeSearch(data, page)

    def executeSearch(self, data, page=0):
        self.es = Elasticsearch(self.es_url)
        search_results = self.es.search(index=self.index, body=data, from_=page*self.size, size=self.size)
        item_results = []
        total_results = 0
        if 'hits' in search_results and search_results['hits']['total']:
            total_results = search_results['hits']['total']
            for item in search_results['hits']['hits']:
                item_results.append(item['_source'])

        final_search_results = {
                "total": total_results,
                "items": item_results
                }
        
        return final_search_results

    def unindexItem(self):
        try:
            self.es = Elasticsearch(self.es_url)
            self.es.delete(index=self.index,doc_type='item',id=self.query,refresh=True)
        except Exception,err:
            print str(err)
        return True

    '''
        To call other ES apis directly
        TODO: add data support
    '''
    def customQuery(self):
        self.es = Elasticsearch(self.es_url)
        resp = requests.get(string.rstrip(self.es_url[0], '/')+'/'+self.query)
        return resp.text

    @staticmethod
    def getSearchCategoriesForApp():
        categories = ['Fiction', 'Childrens', 'Biography', 'Fantasy', 'History', 'Romance', 'Classics', 'Inspirational']
        return categories

    @staticmethod
    def getAllSearchCategories():
        from app import cache
        cache_key = 'search_categories'
        categories = cache.get(cache_key)
        if categories:
            return categories
        categories = []
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT * FROM categories WHERE web_display = 1""")
        for i in range(cursor.rowcount):
            category = Utils.fetchOneAssoc(cursor)
            category = WebUtils.extendCategoryProperties(category)
            categories.append(category)
        cache.set(cache_key, categories)
        return categories

    @async
    def reportFail(self, phrase_fail, query_fail, search_type='free'):
        if self.user_id in Utils.getAdmins() or self.user_id == 0:
            return
        if not phrase_fail and not query_fail:
            return
        elif phrase_fail and not query_fail:
            fail_type = 'phrase_match'
        else:
            fail_type = search_type

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM search_fails WHERE query = %s AND uuid
            = %s""", (self.query, self.uuid))
        if not cursor.fetchone():
            cursor.execute("""INSERT INTO search_fails (user_id, query, type, flow, gcm_id, uuid) 
                    VALUES (%s,%s,%s,%s,%s,%s)""",
                (self.user_id, self.query, fail_type, self.flow, self.gcm_id, self.uuid))
            conn.commit()
        return

    # NOTE Deprecated
    # DELETE This next time
    def getContentData(self, key=None):
        client = MongoClient(webapp.config['MONGO_DB'])
        db = client.ostrich
        refined_content = []
         
        self.es = Elasticsearch(self.es_url)
        for content in db.content.find():
            docs = self.es.mget(index=self.index, doc_type='item', body={"ids":content['items']})
            item_list = []
            if 'docs' in docs:
                for doc in docs['docs']:
                    if '_source' in doc:
                        item_list.append(doc['_source'])
                content['items'] = item_list
                content['_id'] = str(content['_id'])
                refined_content.append(content)
        if not key:
            return refined_content
        else:
            return [_ for _ in refined_content if _['key'] == key][0]['items']

    def mostRecommended(self):
        self.query = [4648, 9, 16, 4026, 4603, 4051, 306, 311, 87, 133, 79, 305, 4576, 50, 5788, 18304, 177]
        return self.fetchResultsFromMYSQL(0, "AND i.item_id in (%s)"%self.str_util(item_ids))

        item_ids = { "ids": self.query }
        reco_list = []
        docs = self.es.mget(index=self.index, doc_type='item', body=item_ids)
        if 'docs' in docs:
            for doc in docs['docs']:
                if '_source' in doc:
                    reco_list.append(doc['_source'])
    
        return reco_list

    def mostSearched(self):
        self.query = [3963, 66, 299, 287, 644, 51, 143, 2058, 4089, 1, 347]
        return self.fetchResultsFromMYSQL(0, "AND i.item_id in (%s)"%self.str_util(item_ids))

        item_ids = { "ids": self.query }
        most_searched = []
        docs = self.es.mget(index=self.index, doc_type='item', body=item_ids)
        if 'docs' in docs:
            for doc in docs['docs']:
                if '_source' in doc:
                    most_searched.append(doc['_source'])
        return most_searched

    def getById(self, item_ids):
        return self.fetchResultsFromMYSQL(0, "AND i.item_id in (%s)"%self.str_util(item_ids))

        result_list = []
        docs = self.es.mget(index=self.index, doc_type='item', body={"ids": item_ids})
        if 'docs' in docs:
            for doc in docs['docs']:
                if '_source' in doc:
                    result_list.append(doc['_source'])
        return result_list


    @staticmethod
    @async
    def logSearch(data, search_type):
        data['timestamp'] = str(datetime.now()).split(".")[0] 
        client = MongoClient(webapp.config['MONGO_DB'])
        db = client.ostrich
        if search_type == "auto":
            db.autocomplete_search_log.insert_one(data)
        else:
            db.search_log.insert_one(data)

