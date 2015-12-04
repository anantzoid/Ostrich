from elasticsearch import Elasticsearch
import MySQLdb
import json
import requests
import os
import unicodedata

class Search():
    def __init__(self, url):
        self.es_url = url.split(',')
        self.es = Elasticsearch(self.es_url)
        self.es_index = 'items'
        self.es_doctype = 'item'

        self.error_log = '/var/log/app_logs/es_script.log'

    def getCursor(self):
        conn = MySQLdb.connect("52.74.20.228","root","root","appdb")
        cursor = conn.cursor()
        return cursor


    def indexById(self, item_id):
        #TODO handle NotFoundError
        indexed_data = self.es.get(index=self.es_index, doc_type=self.es_doctype, id=item_id)
        self.indexDataField('num_ratings', item_id, indexed_data)

    def indexAllFromDB(self):
        indexed_data = self.es.search(index=self.es_index, doc_type=self.es_doctype, size = 3000000)

        if 'hits' not in indexed_data:
            return
        else:
            if 'hits' not in indexed_data['hits']:
                return

        print indexed_data['hits']['total']
        for record in indexed_data['hits']['hits']:
            item_id = int(record['_id'])
            self.indexDataField('num_ratings', item_id, record)
        
    def indexDataField(self, field, item_id, record):
        cursor = self.getCursor()
        print item_id

        data = record['_source']
        cursor.execute("SELECT %s FROM items WHERE item_id = %d"
                %(field, item_id))
        result = cursor.fetchone()
        data[field] = result[0]

        data = json.dumps(data)
        es_resp = self.es.index(index = self.es_index, doc_type=self.es_doctype, id=item_id, body=data)
        return es_resp

    def newIndex(self, index_name, limit, query_condition=''):
        cursor = self.getCursor()

        cursor.execute("SELECT i.item_id, i.item_name, i.price, i.author, i.ratings, \
                i.num_ratings, i.ISBN_10, \
                (select group_concat(c.category_name SEPARATOR '|') FROM categories c \
                INNER JOIN items_categories ic ON ic.category_id = c.category_id WHERE ic.item_id = i.item_id) AS categories \
                FROM items i %s limit %s" % (query_condition, limit))

        results = cursor.fetchall()
      
        f = open(self.error_log, 'a')
        for res in results:

            item_id = int(res[0])
            print item_id
            price  = float(res[2]) if res[2] else 0
            num_ratings = int(res[5])
            
            categories = []
            if res[7]:
                categories = res[7].split("|")
                categories.remove("books")

            #Handles non unicode characters
            item_name = unicodedata.normalize('NFKD', unicode(res[1], "latin-1"))

            data = {
                    "item_id": item_id,
                    "item_name": item_name,
                    "price": price,
                    "ratings": res[4],
                    "author": res[3],
                    "item_type" : "book",
                    "categories": categories,
                    "num_ratings": num_ratings,
                    "isbn": res[6]
                    }

            try:

                data = json.dumps(data)
            except Exception, e:
                print >>f, str(e),"------>", data
                continue
            try:
                resp = self.es.index(index=index_name, doc_type=self.es_doctype, id=item_id, body=data, refresh=True)
            except Exception, e:
                #self.curlIndex(data)
                print >>f, str(e), "=====>", data
                print item_id, str(e)

    def putMapping(self):
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../config/search_mapping.json')) as json_file:
            mapping_data = json.load(json_file) 
        self.es.put_mapping(index=self.es_index, doc_type=self.es_doctype, body=mapping_data)

    
    def indexFromFile(self, filename):
        itemids = []
        with open(filename, 'r') as f:
            for item_id in f.readlines():
                itemids.append(item_id.replace('\n', ''))

        query_condition = " where i.item_id in (%s)"%(','.join(itemids))
        self.newIndex('items', '100000', query_condition)

prod_url = 'https://search-darthvader-4vmjlechafg3wwswxfpqp4xity.us-west-2.es.amazonaws.com'
local_url = 'http://localhost:9200'
Search(prod_url).newIndex('items', '10000', 'where i.item_name like "%harry%"')
#Search(local_url).indexFromFile('/home/ubuntu/utf_ids.txt')
