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

    def getObj(self):
        item_obj = vars(self)
        item_obj = item_obj['data']
        #TODO move these conversions to implicit mysqldb converters
        if item_obj['price']:
            item_obj['price'] = float(item_obj['price'])
        return item_obj

    @staticmethod
    def storeItemRequest(title, author, user_id):
        # This would be rarely used theoretically
        # only when the user will be puttin an item on rent
        # not present in our DB
        #TODO store these requests in a different table too for monitoring??
        
        '''
        if len(item_id) > 10:
            isbn = 'ISBN_10'
        else:
            isbn = 'ISBN_13'
        '''

        conn = mysql.connect()
        store_request_cursor = conn.cursor()
        store_request_cursor.execute("""INSERT INTO item_requests (title, author, user_id) VALUES 
                (%s, %s, %s)""",(title, author, user_id))
        conn.commit()
        insert_id = store_request_cursor.lastrowid
        
        '''
        #TODO map item_type to category_id somehow
        category_id = 1
        store_request_cursor.execute("INSERT INTO items_categories (item_id, category_id) \
                VALUES (%d, %d)" % (insert_id, category_id))
        conn.commit()
        store_request_cursor.close()
        '''
        return True

    @staticmethod
    def removeItem(item_id):
        from app.models import Search
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""UPDATE items SET active = 0 WHERE item_id = %s""",(item_id,))
        conn.commit()
        Search(item_id).unindexItem() 

