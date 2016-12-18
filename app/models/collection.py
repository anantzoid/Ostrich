from app import mysql, webapp
from app.models import *
from app.scripts import Indexer
import json
from slugify import slugify

class Collection(Prototype):
    def __init__(self, collection_id):
        self.data = self.getData(collection_id)
    
    def getData(self, collection_id):
        from app import cache
        cache_key = 'collection_'+str(collection_id)
        collection_data = cache.get(cache_key)
        if collection_data:
            return collection_data

        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT c.*, 
            (select group_concat(ci.item_id order by ci.sort_order asc separator ',') from collections_items ci 
            where ci.collection_id = c.collection_id) as item_ids,
            (select group_concat(concat(cm.meta_key,":",cm.meta_value) separator '&') from collections_metadata cm 
            where cm.collection_id = c.collection_id) as metadata
            FROM collections c WHERE c.collection_id = %s""", (collection_id,))
        data = Utils.fetchOneAssoc(cursor)

        if data['metadata']:
            collections_metadata_raw = data['metadata']
            data['metadata'] = {}
            for props in collections_metadata_raw.split('&'):
                props_formatted = props.split(':')
                data['metadata'][props_formatted[0]] = props_formatted[1]

        if data['item_ids']:
            data['item_ids'] = [int(_) for _ in data['item_ids'].split(',')]
            data['items'] = Search().getById(data['item_ids']) 
        else:
            data['items'] = []

        if not data:
            data = {}
        cache.set(cache_key, data)
        return data

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
                    items = Collection(col_id).getObj()
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

    @staticmethod
    def saveCollectionData(data, collection_item_ids=''):
        conn = mysql.connect()
        cursor = conn.cursor()
        slug_url = slugify(data['name'])[:100] 
        if not int(data['collection_id']):
            cursor.execute("""INSERT INTO collections (name, description, price,
                return_days, partial_order, category_id, slug_url) VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
                (data['name'], data['description'], data['price'], data['return_days'], 
                    data['partial_order'], data['category_id'], slug_url))
            conn.commit()
            collection_id = cursor.lastrowid
        else:
            collection_id = data['collection_id']

        cursor.execute("""UPDATE collections SET name = %s, description = %s,
            price = %s, return_days = %s, category_id = %s, date_edited = CURRENT_TIMESTAMP,
            partial_order = %s, slug_url = %s WHERE collection_id = %s""", (
                data['name'],
                data['description'],
                data['price'],
                data['return_days'],
                data['category_id'],
                data['partial_order'],
                slug_url,
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
       
        original_items = collection_item_ids
        for item in data['items'].split(";"):
            key, value = item.split(":")
            key = int(key)
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

        Indexer().indexCollections(query_condition='c.collection_id='+str(collection_id))
        #NOTE for start session cals
        if collection_id in [4, 5]:
            Notifications().startDataUpdate() 

        from app import cache
        cache_key = 'collection_'+str(collection_id)
        cache.set(cache_key, None)
        return True

    @staticmethod
    def removeCollection(collection_id):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""UPDATE collections SET active = 0, date_edited = CURRENT_TIMESTAMP
            WHERE collection_id = %s""", (collection_id,))
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
    def getHomepageCollections(items=False):
        # List of collections to be displayed on homepage
        from app import cache
        cache_key = 'homepage_collections'+('_items' if items else '')
        homepage_collections = cache.get(cache_key)
        if homepage_collections:
            return homepage_collections

        # NOTE temp
        if webapp.config['APP_ENV'] != 'dev':
            homepage_collection_ids = [38, 40, 41, 42]
        else:
            homepage_collection_ids = [25, 26, 27, 28]
            homepage_collection_ids = [38, 40, 41, 42]
        homepage_collections = []
        for col_id in homepage_collection_ids:
            col_obj = Collection(col_id)
            if items:
                col_obj = col_obj.getObj()
                col_obj['items'] = WebUtils.extendItemWebProperties(col_obj['items'])
                # NOTE temp case
                col_obj['items'] = col_obj['items'][:5]
            else:
                col_obj = col_obj.getObj()

            url = webapp.config['HOST'] + '/books/collection/' + str(col_obj['collection_id']) 

            if col_obj['slug_url']:
                url = url + '-' + col_obj['slug_url']
            col_obj['slug_url'] = url

            if col_obj['image']:
                col_obj['image'] = webapp.config['S3_HOST'] + 'website/collections/' + col_obj['image'] 

            more_url = '/books/category' + col_obj['more_url'] if col_obj['more_url'] else '' 
            col_obj['more_url'] = webapp.config['HOST'] + more_url 
            homepage_collections.append(col_obj)
        if not items:
            mock_collection = {
                    'slug_url': webapp.config['HOST'] + '/books',
                    'collection_id': 0,
                    'name': 'Browse',
                    'image': webapp.config['S3_HOST'] + 'website/collections/Browse.png' 
                    }
            homepage_collections = [mock_collection] + homepage_collections
        cache.set(cache_key, homepage_collections)
        return homepage_collections

