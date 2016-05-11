from app import mysql, webapp
from app.models import *

class Item(Prototype):
    def __init__(self, item_id):
        self.getData(item_id) 

    def getData(self, item_id):
        #TODO cache this
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
            self.data['categories'] = self.data['categories'].split("|") if self.data['categories'] else []

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
    def fetchCategoryById(category_id):
        from app import cache
        cache_key = 'category_'+str(category_id)
        category = cache.get(cache_key)
        if not category:
            cursor = mysql.connect().cursor()
            cursor.execute("SELECT * FROM categories WHERE category_id = %s", (category_id,))
            category = Utils.fetchOneAssoc(cursor)
            cache.set(cache_key, category)
        return category

    @staticmethod
    def getCustomProperties(item_ids, collection=None):
        default_return_days = webapp.config['DEFAULT_RETURN_DAYS']

        if collection:
            if collection['price']:
                collection_custom_data = {'custom_price': collection['price'], 'custom_return_days': collection['return_days'] if collection['return_days'] else default_return_days}
                return collection_custom_data

        charges, days = [], []
        for item_id in item_ids:
            item = Item(item_id).getObj() if isinstance(item_id, int) else item_id
            if item['categories'] and 'Comics' in item['categories']:
                charges.append(100)
                days.append(14)
            else:
                if item['price'] > 900:
                    if Item.checkStock(item['item_id']):
                        charges.append(int(0.15 * item['price']))
                    else:
                        charges.append(int(0.2 * item['price']))
                elif item['price'] > 700:
                    charges.append(99)
                elif item['price'] > 500:
                    charges.append(80)
                elif item['price'] >= 250:
                    charges.append(60)
                else:
                    charges.append(45)
                days.append(default_return_days)
        return {'custom_price': sum(charges), 'custom_return_days': max(days)}

    @staticmethod
    def getExtendRentalChargesSlab(order_data):
        if order_data['from_collection']:
            rental = order_data['collection']['price']
        else:
            rental = order_data['all_charges'][-1]['charge']

        return {
                '7': Utils.getSlabbedAmount(rental, 0.3),
                '10': Utils.getSlabbedAmount(rental, 0.5),
                '14': Utils.getSlabbedAmount(rental, 0.7)
                }
        

    @staticmethod
    def checkStock(item_id):
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT COUNT(*) FROM inventory WHERE item_id = %s
            AND in_stock = 1""",(item_id,))
        stock = cursor.fetchone()
        if stock and int(stock[0]) > 0:
            return True
        return False

    @staticmethod
    def removeItem(item_id):
        from app.models import Search
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""UPDATE items SET active = 0 WHERE item_id = %s""",(item_id,))
        conn.commit()
        Search(item_id).unindexItem() 

    @staticmethod
    def getItemPageUrl(item):
        item_url = webapp.config['HOST']  + '/book/rent/' + str(item['item_id'])
        # NOTE remove this later. Only for Test environment becuase we're poor
        try:
            if item['slug_url']:
                item_url += '-' + item['slug_url']
        except:
            pass
        return item_url
            
