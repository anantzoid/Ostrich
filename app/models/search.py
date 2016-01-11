from app import mysql
from app import webapp
from app.models import Item
from elasticsearch import Elasticsearch
import requests
import string

class Search():
    def __init__(self, query, size=20):
        self.es_url  = webapp.config['ES_NODES'].split(',')
        self.es = Elasticsearch(self.es_url)
        self.query = query
        self.index = 'items_alias'
        self.size = size
        self.switchToRating = False
        self.relevance_functions = [{
                "field_value_factor": {
                    "field": "num_ratings_int"
                    }
                }]


    def basicSearch(self, page=0):
        if self.switchToRating:
            data = {
                    "query": {
                        "function_score": {
                            "query": {
                                "query_string": {
                                    "query": self.query
                                    }
                                },
                            "functions": self.relevance_functions
                            }
                        }
                    }
        else:
            data = {
                    "query": {
                        "query_string": {
                            "query": self.query
                            }
                        }
                    }

        return self.executeSearch(data, page)


    def categorySearch(self, page=0):
        # NOTE temp. Figure out why it only searches for lower case
        self.query = self.query.lower()

        if self.switchToRating:
            data = {
                    "query": {
                        "function_score": {
                            "query": {
                                "match": {
                                    "categories": self.query
                                    }
                                },
                            "functions": self.relevance_functions
                            }
                        }
                    }
        else:
            data = {
                    "query": {
                        "match": {
                            "categories": self.query
                            }
                        }
                    }
        return self.executeSearch(data, page)

    def isbnSearch(self, page=0):
        if self.switchToRating:
            data = {
                    "query": {
                        "function_score": {
                            "query": {
                                "multi_match": {
                                    "query": self.query,
                                    "fields":["isbn_10", "isbn_13"]
                                    }
                                }
                            },
                        "functions": self.relevance_functions
                        }
                    }
        else:
            data = {
                    "query": {
                        "multi_match": {
                            "query": self.query,
                            "fields":["isbn_10", "isbn_13"]
                            }
                        }
                    }

        return self.executeSearch(data, page)


    def executeSearch(self, data, page):
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
        categories = ['Fiction', 'Biography', 'Fantasy', 'History', 'Romance', 'Classics', 'Comics', 'Inspirational', 'Thriller']
        return categories

    @staticmethod
    def reportFail(user_id, q, q_type):
        conn = mysql.connect()
        cursor = conn.cursor()
        q = q.replace('"',"'")
        cursor.execute("""INSERT INTO search_fails (user_id, query, type) VALUES (%d,"%s","%s")
        """ %(user_id, q, q_type))
        conn.commit()
        return

    def mostRecommended(self):
        self.query = [4648, 9, 16, 4026, 4603, 4051, 347, 311, 87, 133]
        item_ids = { "ids": self.query }
        reco_list = []
        docs = self.es.mget(index=self.index, doc_type='item', body=item_ids)
        if 'docs' in docs:
            for doc in docs['docs']:
                if '_source' in doc:
                    reco_list.append(doc['_source'])
    
        return reco_list

    def mostSearched(self):
        self.query = [3963, 66, 299, 287, 644, 51, 143]
        item_ids = { "ids": self.query }
        most_searched = []
        docs = self.es.mget(index=self.index, doc_type='item', body=item_ids)
        if 'docs' in docs:
            for doc in docs['docs']:
                if '_source' in doc:
                    most_searched.append(doc['_source'])
        return most_searched


    '''
        MySQL searches
    '''
    @staticmethod
    def searchQuery(q, page=1):

        limit = page * 20
        offset = (page-1) *20

        connect = mysql.connect()
        search_cursor = connect.cursor()
        search_cursor.execute("SELECT item_id FROM items WHERE item_name LIKE \
                '%%%s%%' OR author LIKE '%%%s%%' LIMIT %d OFFSET %d" %(q, q, limit, offset))
        results = search_cursor.fetchall()
        search_cursor.close()

        refined_results = []
        for item_id in results:
            item = Item(item_id[0])
            refined_results.append(item.getObj())

        return refined_results

        search_cursor = self.connect.cursor()
        search_cursor.execute("SELECT i.item_id FROM items i \
                        LEFT JOIN items_categories ic ON i.item_id = ic.item_id \
                        LEFT JOIN categories c ON c.category_id = ic.category_id \
                        WHERE c.category_name LIKE '%%%s%%' LIMIT %d" %(q, 200-len(refined_results))) 
        results = search_cursor.fetchall()
        search_cursor.close()

        for item_id in results:
            if len(refined_results) <= 20:
                item = Item(item_id[0])
                refined_results.append(item_id.getObj())

        return refined_results        


    @staticmethod
    def searchQueryByType(q, qtype, page=1):

        limit = page * 20
        offset = (page-1) *20

        if qtype == "title":
            query = "SELECT item_id FROM items WHERE item_name LIKE \
                '%%%s%%' LIMIT %d OFFSET %d"
        elif qtype == "genre":
            query = "SELECT i.item_id FROM items i \
                LEFT JOIN items_categories ic ON i.item_id = ic.item_id \
                LEFT JOIN categories c ON c.category_id = ic.category_id \
                WHERE c.category_name LIKE '%%%s%%' LIMIT %d OFFSET %d"

        connect = mysql.connect()
        search_cursor = connect.cursor()
        search_cursor.execute(query % (q, limit, offset))
        results = search_cursor.fetchall()
        search_cursor.close()

        refined_results = []
        for item_id in results:
            item = Item(item_id[0])
            refined_results.append(item.getObj())


        return refined_results


