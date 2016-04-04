from app import mysql
import json
from app.models import Prototype, Utils, Search

class Collection(Prototype):
    def __init__(self, collection_id):
        self.getData(collection_id)
    
    def getData(self, collection_id):
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT c.*, 
            (select group_concat(ci.item_id separator ',') from collections_items ci 
            where ci.collection_id = c.collection_id and ci.active = 1) as item_ids,
            (select group_concat(concat(cm.meta_key,":",cm.meta_value) separator '&') from collections_metadata cm 
            where cm.collection_id = c.collection_id) as metadata
            FROM collections c WHERE c.collection_id = %s""", (collection_id,))
        self.data = Utils.fetchOneAssoc(cursor)
        
        if self.data['metadata']:
            collections_metadata_raw = self.data['metadata']
            self.data['metadata'] = {}
            for props in collections_metadata_raw.split('&'):
                props_formatted = props.split(':')
                self.data['metadata'][props_formatted[0]] = props_formatted[1]
        if not self.data:
            self.data = {}
  
    def getExpandedObj(self):
        collection_object = self.getObj()
        if collection_object['item_ids']:
            collection_object['item_ids'] = [int(_) for _ in collection_object['item_ids'].split(',')]
            collection_object['items'] = Search().getById(collection_object['item_ids']) 
        else:
            collection_object['items'] = []
        return collection_object

    @staticmethod
    def getByItemId(item_id):
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT c.price FROM collections c INNER JOIN 
            collections_items ci ON ci.collection_id = c.collection_id
            WHERE ci.item_id = %s""", (item_id,))
        rental_price = cursor.fetchone()
        if rental_price:
            rental_price = int(rental_price[0])
        return rental_price 

    @staticmethod
    def saveCollectionData(data):
        data = json.loads(data['data'])
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""UPDATE collections SET name = %s, description = %s,
            price = %s, return_days = %s, date_edited = CURRENT_TIMESTAMP
            WHERE collection_id = %s""", (
                data['name'],
                data['description'],
                data['price'],
                data['return_days'],
                data['collection_id'])) 
        conn.commit()

        cursor.execute("""DELETE FROM collections_metadata WHERE collection_id = %s""",
                (data['collection_id'],))
        conn.commit()

        metadata_pairs = []
        for key, value in data['metadata'].iteritems():
            metadata_pairs.append(tuple([data['collection_id'], key, value]))
        cursor.executemany("""INSERT INTO collections_metadata (collection_id, meta_key, meta_value) 
                VALUES (%s, %s, %s)""", metadata_pairs)
        conn.commit()

        item_order = []
        for key, value in data['items'].iteritems():
            item_order.append(tuple([value, data['collection_id'], key]))
        cursor.executemany("""UPDATE collections_items SET sort_order = %s, 
            date_edited = CURRENT_TIMESTAMP WHERE collection_id = %s AND item_id = %s""",
            item_order)
        conn.commit()
        
        format_chars = ",".join(["%s"] * len(data['items'].keys()))
        cursor.execute("""UPDATE collections_items SET active = 0, sort_order = 1000, date_edited = CURRENT_TIMESTAMP
            WHERE collection_id = %s AND item_id NOT IN ("""+format_chars+""")""", 
            (tuple([data['collection_id']]) + tuple(data['items'].keys())))
        conn.commit()
        return True

    @staticmethod
    def removeCollection(collection_id):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""UPDATE collections SET active = 0, date_edited = CURRENT_TIMESTAMP
            WHERE collection_id = %s""", (collection_id))
        conn.commit()
        return True
            
