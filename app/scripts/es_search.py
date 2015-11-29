from elasticsearch import Elasticsearch
import MySQLdb
import json
import requests
import os

class Search():
    def __init__(self, url):
        self.es_url = url.split(',')
        self.es = Elasticsearch(self.es_url)
        self.es_index = 'items'
        self.es_doctype = 'item'

    def getCursor(self):
        conn = MySQLdb.connect("localhost","root","root","appdb")
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
        
    def indexDataField(self, field, tem_id, record):
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

    def newIndex(self, index_name, limit):
        cursor = self.getCursor()
        cursor.execute("SELECT i.item_id, i.item_name, i.price, i.author, i.ratings, \
                i.num_ratings, i.ISBN_10, \
                (select group_concat(c.category_name SEPARATOR '|') FROM categories c \
                INNER JOIN items_categories ic ON ic.category_id = c.category_id WHERE ic.item_id = i.item_id) AS categories \
                FROM items i limit %s" % (limit))

        results = cursor.fetchall()
      
        f = open('/home/ubuntu/es_error.txt', 'w')
        for res in results:

            item_id = int(res[0])
            print item_id
            price  = float(res[2]) if res[2] else 0
            num_ratings = int(res[5])
            
            categories = []
            if res[7]:
                categories = res[7].split("|")
                categories.remove("books")


            data = {
                    "item_id": item_id,
                    "item_name": res[1],
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
                resp = self.es.index(index=index_name, doc_type='item', id=item_id, body=data, refresh=True)
            except Exception, e:
                #self.curlIndex(data)
                print >>f, str(e), "=====>", data
                print item_id, str(e)

    def putMapping(self, index_name):
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../config/search_mapping.json')) as json_file:
            mapping_data = json.load(json_file) 
        self.es.put_mapping(index=index_name, doc_type='item', body=mapping_data)


prod_url = 'https://search-darthvarder-l6yp4bk44zqjzu22o53nqxaxwa.ap-southeast-1.es.amazonaws.com/'
local_url = 'http://localhost:9200'
Search(local_url).newIndex('items', '10000')
