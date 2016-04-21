from app import mysql, webapp
from app.models import *

class Item(Prototype):
    def __init__(self, item_id):
        self.getData(item_id) 

    def getData(self, item_id):
        obj_cursor = mysql.connect().cursor()
        query = """SELECT i.*,
        (select group_concat(c.category_name SEPARATOR '|') FROM categories c 
        INNER JOIN items_categories ic ON ic.category_id = c.category_id WHERE 
        ic.item_id = i.item_id) AS categories
        FROM items i WHERE i.active=1 AND i.item_id = %s"""

        obj_cursor.execute(query, (item_id,))
        self.data = Utils.fetchOneAssoc(obj_cursor)
        if not self.data:
            self.data = {}
        else:
            self.data['price'] = float(self.data['price']) if self.data['price'] else self.data['price']

    def getObj(self):
        item_obj = vars(self)
        item_obj = item_obj['data']
        #TODO move these conversions to implicit mysqldb converters
        if item_obj and item_obj['price']:
            item_obj['price'] = float(item_obj['price'])
        return item_obj

    @staticmethod
    def storeItemRequest(data):
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
        title = Utils.getParam(data, 'title')
        author = Utils.getParam(data, 'author')
        user_id = Utils.getParam(data, 'user_id', 'int')
        query = Utils.getParam(data, 'related_search')
    
        conn = mysql.connect()
        store_request_cursor = conn.cursor()
        store_request_cursor.execute("""INSERT INTO item_requests (title, author, user_id, query) VALUES 
                (%s, %s, %s, %s)""",(title, author, user_id, query))
        conn.commit()
        insert_id = store_request_cursor.lastrowid
        
        Utils.notifyAdmin(user_id, "Item Request: "+title)
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
    def getCustomProperties(item_ids, collection=None):
        default_return_days = webapp.config['DEFAULT_RETURN_DAYS']

        if collection:
            if collection['price']:
                collection_custom_data = {'price': collection['price'], 'return_days': collection['return_days'] if collection['return_days'] else default_return_days}
                return collection_custom_data

        charges, days = [], []
        for item_id in item_ids:
            item = Item(item_id).getObj() if isinstance(item_id, int) else item_id
            if item['categories'] and 'Comics' in item['categories']:
                charges.append(100)
                days.append(14)
            elif item['price'] > 500:
                charges.append(80)
                days.append(default_return_days)
            elif item['price'] >= 250:
                charges.append(60)
                days.append(default_return_days)
            else:
                charges.append(45)
                days.append(default_return_days)
        return {'price': sum(charges), 'return_days': max(days)}

    @staticmethod
    def removeItem(item_id):
        from app.models import Search
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""UPDATE items SET active = 0 WHERE item_id = %s""",(item_id,))
        conn.commit()
        Search(item_id).unindexItem() 

