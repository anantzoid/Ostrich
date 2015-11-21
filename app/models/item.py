from app import mysql
from app.models import Prototype, Utils

class Item(Prototype):
    def __init__(self, item_id):
        self.getData(item_id) 

    def getData(self, item_id):
        obj_cursor = mysql.connect().cursor()
        obj_cursor.execute("SELECT * FROM items WHERE item_id = %d" %(item_id))
        self.data = Utils.fetchOneAssoc(obj_cursor)
        if not self.data:
            self.data = {}
        else:
            self.data['price'] = float(self.data['price']) if self.data['price'] else self.data['price']
            self.data['security_deposit'] = self.getSecurityDepositAmount()


    def getObj(self):
        item_obj = vars(self)
        item_obj = item_obj['data']
        #if item_obj:
        #    item_obj = self.getTempVarsForBookModel(item_obj)

        return item_obj

    def getMinObj(self):
        min_obj = {}
        item_obj = self.getObj()

        min_obj["item_id"] = item_obj["item_id"]
        min_obj["item_name"] = item_obj["title"]
        min_obj["images"] = item_obj["photos"]

        #TODO generic minification: after making BookModel items consistent

        return min_obj


    def getSecurityDepositAmount(self):
        security = 0
        if self.data['price']:
            security = min(1000, 0.5*self.data['price'])

        return security


    def getTempVarsForBookModel(self, item_obj):
        item_obj['isbn'] = item_obj['ISBN_10']
        item_obj['title'] = item_obj['item_name']
        item_obj['cover'] = ''
        item_obj['reviews'] = ''
        item_obj['deposit'] = item_obj['security_deposit']
        item_obj['delivery'] = 0
        item_obj['available_in_hours'] = 3
        item_obj['bound'] = ''
        item_obj['year'] = 2014
        item_obj['photos'] = []
        item_obj['return_days'] = 30
        item_obj['rating_avg'] = int(item_obj['ratings'][0]) if item_obj['ratings'] else 0
        item_obj['rating_numbers'] = item_obj['num_ratings']
        
        del item_obj['ASIN']
        del item_obj['ISBN_10']
        del item_obj['ISBN_13']
        del item_obj['item_name']
        del item_obj['language']
        del item_obj['num_ratings']
        del item_obj['ratings']
        del item_obj['price']
        del item_obj['security_deposit']
        
        return item_obj


    @staticmethod
    def storeItemRequest(item_type, item_id=0, item_name=''):
        # This would be rarely used theoretically
        # only when the user will be puttin an item on rent
        # not present in our DB

        if len(item_id) > 10:
            isbn = 'ISBN_10'
        else:
            isbn = 'ISBN_13'

        conn = mysql.connect()
        store_request_cursor = conn.cursor()
        store_request_cursor.execute("INSERT INTO items (item_name, %s) VALUES \
                ('%s', '%s')" % (isbn, item_name, item_id))
        conn.commit()
        insert_id = store_request_cursor.lastrowid

        #TODO map item_type to category_id somehow
        category_id = 1
        store_request_cursor.execute("INSERT INTO items_categories (item_id, category_id) \
                VALUES (%d, %d)" % (insert_id, category_id))
        conn.commit()
        store_request_cursor.close()

        return True
