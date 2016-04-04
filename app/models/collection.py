from app import mysql
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
    def getPreview():
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT collection_id, name FROM collections WHERE active = 1""")
        num_rows = cursor.rowcount
        collections = []
        for i in range(num_rows):
            collections.append(Utils.fetchOneAssoc(cursor))
        return collections

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
