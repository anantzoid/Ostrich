from elasticsearch import Elasticsearch
from app import webapp
from app import mysql 
from app.models import Utils
import unicodedata

class Indexer():
    def __init__(self, index='items_alias'):
        self.es_url  = webapp.config['ES_NODES'].split(',')
        self.es = Elasticsearch(self.es_url)
        self.es_index = index
        self.es_doctype = 'item'
        #self.err_log = open('es_err.log','w')
 
    def indexItemObject(self, data):
        try:
            resp = self.es.index(index=self.es_index, doc_type=self.es_doctype,
                    id=data['item_id'], body=data, refresh=True)
        except Exception, e:
            #print >>self.err_log, str(e)+","+ str(data['item_id'])
            print str(e), data['item_id']

    def indexItems(self, query_condition='', limit=''):

        search_query = """SELECT i.item_id, i.item_name, i.author, i.price,
        i.ratings, i.num_ratings, i.num_reviews, i.img_small,
        (select group_concat(c.category_name SEPARATOR '|') FROM categories c 
        INNER JOIN items_categories ic ON ic.category_id = c.category_id WHERE 
        ic.item_id = i.item_id) AS categories
        FROM items i WHERE i.active=1"""

        if query_condition:
            search_query += query_condition

        if limit:
            search_query += ' LIMIT '+limit

        cursor = mysql.connect().cursor()
        cursor.execute(search_query)
        
        num_items = cursor.rowcount
        for num in range(num_items):
            record = Utils.fetchOneAssoc(cursor)
            print record['item_id']
            if record['categories'] is not None:
                record['categories'] = record['categories'].split("|")
            else:
                record['categories'] = []
            record = self.fetchItemProperties(record)
            record = self.extendItemProperties(record)
           
            record = self.handleUnicode(record)
            self.indexItemObject(record)
    
    def fetchItemProperties(self, item):
        item['isbn_10'] = []
        item['isbn_13'] = []
        item['in_stock'] = 0

        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT isbn_10, isbn_13 FROM item_isbn WHERE item_id = %s""",
                (item['item_id'],))
        isbn_data = cursor.fetchall()
        for prop in isbn_data:
            if prop[0] is not None:
                item['isbn_10'].append(prop[0])
            if prop[1] is not None:
                item['isbn_13'].append(prop[1])

        cursor.execute("""SELECT COUNT(*) FROM inventory WHERE item_id = %s
            AND in_stock = 1""",(item['item_id'],))
        stock = cursor.fetchone()
        if stock and int(stock[0]) > 0:
            item['in_stock'] = 1

        return item

    def extendItemProperties(self, item):
        item['num_ratings_int'] = 0
        item['num_reviews_int'] = 0

        if item['num_ratings']:
            item['num_ratings_int'] = int(item['num_ratings'].replace(',',''))

        if item['num_reviews']:
            item['num_reviews_int'] = int(item['num_reviews'].replace(',',''))

        #TODO item_name_prettify

        return item

    def handleUnicode(self, item):
        for key in item.keys():
            if isinstance(item[key], unicode):
                item[key] = unicodedata.normalize('NFKD', item[key])
        return item
