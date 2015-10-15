from app import webapp
from app import mysql
import datetime
#from app.models import User, Item

class Order():
    def __init__(self, item_ids, user_id, address_id, order_return=None):
        #self.user = User(user_id)
        #self.item = Item(item_id)

        self.user = user_id
        self.items = item_ids
        self.address_id = address_id
        
        self.order_placed = self.getCurrentTimestamp()
        if not order_return:
            self.order_return = self.getDefaultReturnTimestamp()

        self.connect = mysql.connect()                    

    def placeOrder(self):
       
        #check user validity

        inventory_ids = self.getInventoryIds() 
        
        '''
        #NOTE Skipping this too for now
        #check if user is ordering same item in same period
        if not self.checkOrderValidity():
            return {'message': 'Can only order after returning'}
        '''
                
        insert_data_cursor = self.connect.cursor()
        insert_data_cursor.execute("INSERT INTO orders (user_id, address_id, \
                order_placed, order_return) VALUES(%d, %d, '%s', '%s')" % \
                (self.user, self.address_id, self.order_placed, self.order_return) )
        self.connect.commit()
        order_id = insert_data_cursor.lastrowid
        insert_data_cursor.close()

        for inventory_id in inventory_ids:
            order_history_cursor = self.connect.cursor()
            order_history_cursor.execute("INSERT INTO order_history (inventory_id, order_id) VALUES (%d, %d)" %(inventory_id, order_id))
            self.connect.commit()
            order_history_cursor.close()

            update_stock_cursor = self.connect.cursor()
            update_stock_cursor.execute("UPDATE inventory SET in_stock = 0 WHERE inventory_id = %d" % (inventory_id))
            self.connect.commit()
            update_stock_cursor.close()

        return {'order_id': order_id}
    

    def checkOrderValidity(self):
        check_record_cursor = self.connect.cursor()
        check_record_cursor.execute("SELECT order_id FROM orders WHERE user_id = %d AND item_id = %d AND UNIX_TIMESTAMP(order_return) <= UNIX_TIMESTAMP('%s')" %(self.user, self.item, self.order_placed))
        record_count = check_record_cursor.fetchone()
        check_record_cursor.close()
        return 0 if record_count else 1

    def getInventoryIds(self):
        
        inventory_ids = []
        for item_id in self.items:
            item_check_cursor = self.connect.cursor()
            item_check_cursor.execute("SELECT inventory_id, lender_id FROM inventory \
                    WHERE item_id = %d AND in_stock = 1 ORDER BY date_added" % (item_id))
            inv_items = item_check_cursor.fetchall()
            item_check_cursor.close()

            if inv_items: 
                # check if a lender's item is present,
                # else return the inventory item
                inv_item_selected = inv_items[0][0]
                for item in inv_items:
                    if item[1]:
                        inv_item_selected = item[0]
                        break

                inventory_ids.append(inv_item_selected)
            else:
                #TODO change this logic once we stop incremental inventory
                insert_inv_item = self.connect.cursor()
                insert_inv_item.execute("INSERT INTO inventory (item_id) VALUES ('%s')" %(item_id))
                self.connect.commit()
                new_inv_id = insert_inv_item.lastrowid
                insert_inv_item.close()

                inventory_ids.append(new_inv_id)


        return inventory_ids

    
    def getCurrentTimestamp(self):
        current_timestamp = datetime.datetime.now()
        order_placed = str(current_timestamp).split('.')[0]

        return order_placed


    def getDefaultReturnTimestamp(self):
        current_timestamp = datetime.datetime.now()
        next_week_timestamp = str(current_timestamp + datetime.timedelta(days=7))
        order_return = next_week_timestamp.split('.')[0]

        return order_return
