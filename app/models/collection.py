from app import mysql
from app.models import *
import json

class Collection(Prototype):
    def __init__(self, collection_id):
        self.getData(collection_id)
    
    def getData(self, collection_id):
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT c.*, 
            (select group_concat(ci.item_id order by ci.sort_order asc separator ',') from collections_items ci 
            where ci.collection_id = c.collection_id) as item_ids,
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
    def getByCategory():
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT cc.*,
            (select group_concat(c.collection_id separator ',') from collections c
            where c.category_id = cc.category_id and c.active=1) as collection_ids
            FROM collections_category cc""")
        num_rows = cursor.rowcount
        collections_categories = []
        for i in range(num_rows):
            category = Utils.fetchOneAssoc(cursor)
            category['collections'] = []
            if category['collection_ids'] is not None:
                for col_id in category['collection_ids'].split(','):
                    items = Collection(col_id).getExpandedObj()
                    if items:
                        category['collections'].append(items)
                collections_categories.append(category)
        return collections_categories

    @staticmethod
    def getPreview():
        collections_data = {
                'collections_list': [],
                'collections_categories': []
                }
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT collection_id, name FROM collections WHERE active = 1""")
        num_rows = cursor.rowcount
        collections = []
        for i in range(num_rows):
            collections_data['collections_list'].append(Utils.fetchOneAssoc(cursor))

        cursor.execute("""SELECT category_id, category_name FROM collections_category""")
        num_rows = cursor.rowcount
        collections = []
        for i in range(num_rows):
            collections_data['collections_categories'].append(Utils.fetchOneAssoc(cursor))
        return collections_data

    # NOTE not used anymore
    @staticmethod
    def getCollectionPropertiesByItemId(item_id):
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT c.price, c.return_days FROM collections c INNER JOIN 
            collections_items ci ON ci.collection_id = c.collection_id
            WHERE ci.item_id = %s""", (item_id,))
        rental_data = cursor.fetchone()
        if rental_data:
            rental_data = {'price': int(rental_data[0]), 'return_days': int(rental_data[1])} 
        return rental_data

    @staticmethod
    def saveCollectionData(data, collection_item_ids=''):
        conn = mysql.connect()
        cursor = conn.cursor()
        if not int(data['collection_id']):
            cursor.execute("""INSERT INTO collections (name, description, price,
                return_days, category_id) VALUES (%s, %s, %s, %s, %s)""", 
                (data['name'], data['description'], data['price'], data['return_days'], data['category_id']))
            conn.commit()
            collection_id = cursor.lastrowid
        else:
            collection_id = data['collection_id']

        cursor.execute("""UPDATE collections SET name = %s, description = %s,
            price = %s, return_days = %s, category_id = %s, date_edited = CURRENT_TIMESTAMP
            WHERE collection_id = %s""", (
                data['name'],
                data['description'],
                data['price'],
                data['return_days'],
                data['category_id'],
                collection_id)) 
        conn.commit()

        cursor.execute("""DELETE FROM collections_metadata WHERE collection_id = %s""",
                (collection_id,))
        conn.commit()

        if data['metadata']:
            metadata_pairs = []
            for meta in data['metadata'].split(";"):
                key, value = meta.split(":")
                metadata_pairs.append(tuple([collection_id, key, value]))
            cursor.executemany("""INSERT INTO collections_metadata (collection_id, meta_key, meta_value) 
                    VALUES (%s, %s, %s)""", metadata_pairs)
            conn.commit()

        update_item_order = []
        insert_item_order = []
        item_ids = []
       
        original_items = collection_item_ids.split(",")
        for item in data['items'].split(";"):
            key, value = item.split(":")
            item_ids.append(key)
            if key in original_items:
                update_item_order.append(tuple([value, collection_id, key]))
            else: 
                insert_item_order.append(tuple([value, collection_id, key]))
                
        cursor.executemany("""UPDATE collections_items SET sort_order = %s, 
            date_edited = CURRENT_TIMESTAMP WHERE collection_id = %s AND item_id = %s""",
            update_item_order)
        conn.commit()
        cursor.executemany("""INSERT INTO collections_items (sort_order, collection_id, item_id)
            VALUES (%s, %s, %s)""", insert_item_order)
        conn.commit()
        
        format_chars = ",".join(["%s"] * len(item_ids))
        cursor.execute("""DELETE FROM collections_items 
            WHERE collection_id = %s AND item_id NOT IN ("""+format_chars+""")""", 
            (tuple([collection_id]) + tuple(item_ids)))
        conn.commit()

        #NOTE for start session cals
        if collection_id in [4, 5]:
            Notifications().startDataUpdate() 
        return True

    @staticmethod
    def removeCollection(collection_id):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""UPDATE collections SET active = 0, date_edited = CURRENT_TIMESTAMP
            WHERE collection_id = %s""", (collection_id))
        conn.commit()
        return True
           
    @staticmethod
    def addCategory(data):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO collections_category (category_name, image) VALUES (%s, %s)""", (data['name'], data['img_url']))
        conn.commit()
        response = {'category_name': data['name']}
        response['category_id'] = cursor.lastrowid
        return response
  
    '''
        Website Related functions
    '''
    @staticmethod
    def getHomepageCollections():
        # List of collections to be displayed on homepage
        homepage_collection_ids = [1, 2, 3, 4, 5, 10, 19]
        homepage_collections = []
        for col_id in homepage_collection_ids:
            col_obj = Collection(col_id).getObj()
            if not col_obj['image']:
                col_obj['image'] = '/static/img/book_placeholder.jpeg' 

            col_obj['url'] = webapp.config['HOST'] + col_obj['slug_url'] 
            col_obj['image'] = webapp.config['HOST'] + col_obj['image'] 
            homepage_collections.append(col_obj)
        return homepage_collections

