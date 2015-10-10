from app import webapp
import datetime
#from app.models import User, Item
import MySQLdb

class Order():
    def __init__(self, item_id, user_id, order_return=None):
        #self.user = User(user_id)
        #self.item = Item(item_id)

        self.user = user_id
        self.item = item_id
        
        if not order_return:
            self.order_return = self.getDefaultReturnDate()


    def placeOrder(self):

        #check user validity
        #check item availability

        #check if user is ordering same item in same period

        #TODO beautify SQL calls
        conn = MySQLdb.connect("localhost", "root", "root", "appdb")                    
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (item_id, user_id, order_return) VALUES(%d, %d, '%s')" %(self.item, self.user, self.order_return) )
        conn.commit()
        order_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return order_id


    def getDefaultReturnDate(self):

        current_timestamp = datetime.datetime.now()
        next_week_timestamp = str(current_timestamp + datetime.timedelta(days=7))
        order_return = next_week_timestamp.split('.')[0]

        return order_return
