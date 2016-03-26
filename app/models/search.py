from app import mysql
from app import webapp
from app.models import *
from app.decorators import async
from elasticsearch import Elasticsearch
from pymongo import MongoClient
from datetime import datetime
import requests
import string

class Search():
    def __init__(self, query='', user_info={}, flow='borrow', size=20):
        self.es_url  = webapp.config['ES_NODES'].split(',')
        self.es = Elasticsearch(self.es_url)
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
            self.user_id = user_info['user_id']
            self.gcm_id = user_info['gcm_id']
            self.uuid = user_info['uuid']
        except:
            pass


    def basicSearch(self, page=0):
        phrase_fail = False 
        query_fail = False

        phrase_results = self.matchPhrase(page)
        if len(phrase_results['items']) == 0:
            phrase_fail = True

        if len(phrase_results['items']) in range(11) and len(phrase_results['items']) != 1:
            filter_ids = [_['item_id'] for _ in phrase_results['items']]
            queried_results = self.queryMatch(page, filter_ids)
            if phrase_fail and len(queried_results['items']) == 0 :
                query_fail = True
            phrase_results['items'].extend(queried_results['items'])
            phrase_results['total'] += queried_results['total']
      
        phrase_results['collections'] = self.getCollectionsFromResults(phrase_results['items'])
        self.reportFail(phrase_fail, query_fail)
        return phrase_results

    def matchPhrase(self, page):
        data = self.search_query 
        data["query"]["function_score"]["query"] = {"match_phrase": {"item_name": self.query}} 
        return self.executeSearch(data, page)

    def queryMatch(self, page, filter_ids):
        data = self.search_query 
        data["query"]["function_score"]["query"] = {"filtered": {
                            "query": {"query_string": {"query": self.query}},
                            "filter": {"bool": {"must_not":{"ids":{"values": filter_ids}}}}
                        }}
        return self.executeSearch(data, page)

    def categorySearch(self, page=0):
        data = self.search_query 
        data["query"]["function_score"]["query"] = {"match": {"categories": self.query}} 
        return self.executeSearch(data, page)

    def collectionsSearch(self, page=0):
        data = self.search_query 
        data["query"]["function_score"]["query"] = {"match": {"in_collections": self.query}} 
        return self.executeSearch(data, page)

    def isbnSearch(self, page=0):
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
            collection_objects = self.fetchCollectionObject(collection)
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
            collection_object['items'] = []
            docs = self.es.mget(index=self.index, doc_type='item', body={"ids": collection_object['item_ids']})
            if 'docs' in docs:
                for doc in docs['docs']:
                    if '_source' in doc:
                        collection_object['items'].append(doc['_source'])
        return collection_object
        
    def autoComplete(self, page=0):
        if len(self.query) < 4:
            return {"items": []}
        data = self.search_query
        data["query"]["function_score"]["query"] = {"match_phrase_prefix":{"item_name":self.query}}
        return self.executeSearch(data, page)

    def executeSearch(self, data, page=0):
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
            self.es.delete(index=self.index,doc_type='item',id=self.query,refresh=True)
        except Exception,err:
            print str(err)
        return True

    '''
        To call other ES apis directly
        TODO: add data support
    '''
    def customQuery(self):
        resp = requests.get(string.rstrip(self.es_url[0], '/')+'/'+self.query)
        return resp.text

    @staticmethod
    def getSearchCategories():
        # TODO from mongo
        #  NOTE call session in manager to update
        categories = ['Fiction', 'Biography', 'Fantasy', 'History', 'Romance', 'Classics', 'Inspirational', 'Thriller']
        return categories

    @async
    def reportFail(self, phrase_fail, query_fail, search_type='free'):
        if self.user_id in Utils.getAdmins():
            return
        if not phrase_fail and not query_fail:
            return
        elif phrase_fail and not query_fail:
            fail_type = 'phrase_match'
        else:
            fail_type = search_type

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO search_fails (user_id, query, type, flow, gcm_id, uuid) 
                VALUES (%s,%s,%s,%s,%s,%s)""",
            (self.user_id, self.query, fail_type, self.flow, self.gcm_id, self.uuid))
        conn.commit()
        return

    def getContentData(self, key=None):
        client = MongoClient(webapp.config['MONGO_DB'])
        db = client.ostrich
        refined_content = []
         
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
        item_ids = { "ids": self.query }
        most_searched = []
        docs = self.es.mget(index=self.index, doc_type='item', body=item_ids)
        if 'docs' in docs:
            for doc in docs['docs']:
                if '_source' in doc:
                    most_searched.append(doc['_source'])
        return most_searched

    def getById(self, item_ids):
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


