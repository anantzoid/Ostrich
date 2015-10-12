from app import webapp
from app import mysql
import datetime
#from app.models import User, Item
import MySQLdb

class Order():
    def __init__(self, item_id, user_id, order_return=None):
        #self.user = User(user_id)
        #self.item = Item(item_id)

        self.user = user_id
        self.item = item_id
        
        self.order_placed = self.getCurrentTimestamp()
        if not order_return:
            self.order_return = self.getDefaultReturnTimestamp()

        self.connect = mysql.connect()                    

    def placeOrder(self):
        '''
        Flow:
            Check if user is not blocked
            Check item availability in inventory
            Check if user has currently borrowed the same item
            Place order
            Insert inventory_id and order_id
            Update stock availability
        '''
        
        #check user validity

        inventory_id = self.checkItemAvailability() 
        if not inventory_id:
            return {'message': 'Item out of stock'}


        #check if user is ordering same item in same period
        check_record_cursor = self.connect.cursor()
        check_record_cursor.execute("SELECT order_id FROM orders WHERE user_id = %d AND item_id = %d AND UNIX_TIMESTAMP(order_return) <= UNIX_TIMESTAMP('%s')" %(self.user, self.item, self.order_placed))
        record_count = check_record_cursor.fetchone()
        check_record_cursor.close()

        if record_count:
            return {'message': 'Can only order after returning'}

        insert_data_cursor = self.connect.cursor()
        insert_data_cursor.execute("INSERT INTO orders (item_id, user_id, order_placed, order_return) VALUES(%d, %d, '%s', '%s')" %(self.item, self.user, self.order_placed, self.order_return) )
        self.connect.commit()
        order_id = insert_data_cursor.lastrowid
        insert_data_cursor.close()

        order_history_cursor = self.connect.cursor()
        order_history_cursor.execute("INSERT INTO order_history (inventory_id, order_id) VALUES (%d, %d)" %(inventory_id, order_id))
        order_history_cursor.close()

        update_stock_cursor = self.connect.cursor()
        update_stock_cursor.execute("UPDATE inventory SET in_stock = 0 WHERE inventory_id = %d" % (inventory_id))
        self.connect.commit()
        update_stock_cursor.close()

        return {'order_id': order_id}
    

    def checkItemAvailability(self):
        item_check_cursor = self.connect.cursor()
        item_check_cursor.execute("SELECT inventory_id, lender_id FROM inventory WHERE item_id = %d AND in_stock = 1 ORDER BY date_added" % (self.item))
        items = item_check_cursor.fetchall()
        item_check_cursor.close()
        
        if not items:
            return None
        
        # check if a lender's item is present,
        # else return the inventory item

        for item in items:
            if item[1]:
                return int(item[0]) 

        return int(items[0][0])

    
    def getCurrentTimestamp(self):
        current_timestamp = datetime.datetime.now()
        order_placed = str(current_timestamp).split('.')[0]

        return order_placed


    def getDefaultReturnTimestamp(self):
        current_timestamp = datetime.datetime.now()
        next_week_timestamp = str(current_timestamp + datetime.timedelta(days=7))
        order_return = next_week_timestamp.split('.')[0]

        return order_return
