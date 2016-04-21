from elasticsearch import Elasticsearch
from app import webapp
from app import mysql 
from app.models import Utils, Item
import unicodedata

class Indexer():
    def __init__(self, index='items_alias'):
        self.es_url  = webapp.config['ES_NODES'].split(',')
        self.es = Elasticsearch(self.es_url)
        self.es_index = index
        self.es_doctype = 'item'
        #self.err_log = open('es_err.log','w')

    def indexCollections(self, query_condition):
        #TODO fetch collection object from Collection class
        cursor = mysql.connect().cursor()
        condition = 'WHERE c.partial_order = 0'
        if query_condition:
            condition = ' AND '+query_condition
        cursor.execute("""SELECT c.*,
           (select group_concat(ci.item_id SEPARATOR ',') FROM collections_items ci
           WHERE ci.collection_id = c.collection_id) AS item_ids
           FROM collections c """+condition)
        num_items = cursor.rowcount
        for i in range(num_items):
            collection = Utils.fetchOneAssoc(cursor)
            collection['item_ids'] = [int(_) for _ in collection['item_ids'].split(',')]
            collection['metadata'] = self.fetchCollectionsMetadata(collection['collection_id'])
            try:
                self.es.index(index=self.es_index, doc_type='collections', 
                    id=collection['collection_id'], body=collection, refresh=True)
                self.updateItems(collection['item_ids'], collection['name'])
            except Exception, e:
                print str(e), collection['collection_id']

    def fetchCollectionsMetadata(self, collection_id):
        collections_metadata = {}
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT * FROM collections_metadata WHERE collection_id = %s""",
                (collection_id,))
        metadata = cursor.fetchall()
        for data in metadata:
            collections_metadata[data[1]] = data[2]
        return collections_metadata

    def updateItems(self, item_ids, collection_name):
        #TODO support one item beloning to multiple collections
        update_body = {"doc": {"in_collections":[collection_name]}}
        for item_id in item_ids:
            self.es.update(index=self.es_index, doc_type='item',id=item_id,
                    body=update_body)
        
    def indexItemObject(self, data):
        try:
            resp = self.es.index(index=self.es_index, doc_type=self.es_doctype,
                    id=data['item_id'], body=data, refresh=True)
        except Exception, e:
            #print >>self.err_log, str(e)+","+ str(data['item_id'])
            print str(e), data['item_id']

    def indexItems(self, query_condition='', limit='', custom_keys={}):

        search_query = """SELECT i.item_id, i.item_name, i.author, i.price,
        i.ratings, i.num_ratings, i.num_reviews, i.img_small, i.asin, i.goodreads_id, i.summary,
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
            record = self.fetchItemProperties(record, custom_keys)
            record = self.extendItemProperties(record)
           
            record = self.handleUnicode(record)
            self.indexItemObject(record)
    
    def fetchItemProperties(self, item, custom_keys):
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

        cursor.execute("""SELECT c.collection_id, name FROM collections c
                INNER JOIN collections_items ci ON c.collection_id=ci.collection_id
                WHERE ci.item_id = %s""", (item['item_id'],))
        c_names = cursor.fetchall()
        c_ids = []
        if c_names:
            item['in_collections'] = []
            for c_name in c_names:
                item['in_collections'].append(c_name[1])
                c_ids.append(c_name[0])

        item_custom_props = Item.getCustomProperties([item])
        for prop in item_custom_props.keys():
            item['custom_'+prop] = item_custom_props[prop] 
        
        if custom_keys:
            for key in custom_keys.keys():
                item[key] = custom_keys[key]
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
