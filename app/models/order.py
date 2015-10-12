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

        self.conn = mysql.connect()                    

    def placeOrder(self):

        #check user validity
        #check item availability
        '''
            if (lended or in_inventory) & available
        '''



        #check if user is ordering same item in same period
        check_record_cursor = self.conn.cursor()
        check_record_cursor.execute("SELECT COUNT(*) FROM orders WHERE user_id = %d AND item_id = %d AND UNIX_TIMESTAMP(order_return) <= UNIX_TIMESTAMP('%s')" %(self.user, self.item, self.order_placed))
        record_count = check_record_cursor.fetchone()
        check_record_cursor.close()

        if not record_count:
            insert_data_cursor = conn.cursor()
            insert_data_cursor.execute("INSERT INTO orders (item_id, user_id, order_placed, order_return) VALUES(%d, %d, '%s', '%s')" %(self.item, self.user, self.order_placed, self.order_return) )
            conn.commit()
            order_id = insert_data_cursor.lastrowid
            insert_data_cursor.close()


            return {'order_id': order_id}
        else:
            return {'message': 'Can only order after returning'}
    

    def checkItemAvailability(self):
        item_check_cursor = self.connect.cursor()
        item_check_cursor.execute("SELECT inventory_id, lender_id FROM inventory WHERE item_id = %d AND in_stock = 1 ORDER BY date_added" % (self.item))
        items = item_check_cursor.fetchall()

        #allocation of item:
        #LRU lender
        #LRU date added in inventory

    
    def getCurrentTimestamp(self):

        current_timestamp = datetime.datetime.now()
        order_placed = str(current_timestamp).split('.')[0]

        return order_placed


    def getDefaultReturnTimestamp(self):

        current_timestamp = datetime.datetime.now()
        next_week_timestamp = str(current_timestamp + datetime.timedelta(days=7))
        order_return = next_week_timestamp.split('.')[0]

        return order_return
