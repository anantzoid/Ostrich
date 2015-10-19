from app import webapp
from app import mysql
import datetime
#from app.models import User, Item

class Order():
    def __init__(self, order_id):
        self.order_id = order_id
        

    @staticmethod
    def placeOrder(item_ids, user_id, address_id, order_return=None):
       
        order_placed = getCurrentTimestamp()
        if not order_return:
            order_return = getDefaultReturnTimestamp()

        #check user validity
        #check order validity
        
        '''
        #NOTE Skipping this too for now
        #check if user is ordering same item in same period
        if not self.checkOrderValidity():
            return {'message': 'Can only order after returning'}
        '''

        connect = mysql.connect() 
        insert_data_cursor = connect.cursor()
        insert_data_cursor.execute("INSERT INTO orders (user_id, address_id, \
                order_placed, order_return) VALUES(%d, %d, '%s', '%s')" % \
                (user_id, address_id, order_placed, order_return) )
        connect.commit()
        order_id = insert_data_cursor.lastrowid
        order = Order(order_id)
        insert_data_cursor.close()

        order.updateInventoryPostOrder(item_ids)
        #TODO call roadrunnr api
        #TODO send user order confirmation notification

        return {'order_id': order.order_id}
    

    def updateInventoryPostOrder(self, item_ids):
        inventory_ids = self.getInventoryIds(item_ids) 

        #update order_history and clear stock in inventory
        connect = mysql.connect()
        for inventory_item in inventory_ids:
            order_history_cursor = connect.cursor()
            order_history_cursor.execute("INSERT INTO order_history (inventory_id, \
                    order_id) VALUES (%d, %d)" %(inventory_item['inventory_id'], self.order_id))
            connect.commit()
            order_history_cursor.close()


            update_stock_cursor = connect.cursor()
            update_stock_cursor.execute("UPDATE inventory SET in_stock = 0 WHERE \
                    inventory_id = %d" % (inventory_item['inventory_id']))
            connect.commit()
            update_stock_cursor.close()


            #add credits to lender
            #TODO credits based on business logic
            item_credits = 0
            add_credit_cursor = connect.cursor()
            add_credit_cursor.execute("INSERT INTO lender_credits (lender_id, \
                    order_id, inventory_id, credits, redeemed) VALUES (%d, %d, \
                    %d, %d, %d)" %(inventory_item['lender_id'], self.order_id, \
                    inventory_item['inventory_id'], item_credits, 0))
            connect.commit()
            add_credit_cursor.close()

            #TODO send notification to lender

             

    def getInventoryIds(self, item_ids):
        
        inventory_ids = []
        for item_id in item_ids:
            item_check_cursor = self.connect.cursor()
            item_check_cursor.execute("SELECT inventory_id, lender_id FROM inventory \
                    WHERE item_id = %d AND in_stock = 1 ORDER BY date_added" % (item_id))
            inv_items = item_check_cursor.fetchall()
            item_check_cursor.close()

            if inv_items: 
                # check if a lender's item is present,
                # else return the inventory item
                item_selected = list(inv_items[0])
                for item in inv_items:
                    if item[1]:
                        item_selected = item
                        break

                inventory_ids.append({
                    'inventory_id': item_selected[0],
                    'lender_id': item_selected[1]
                    })
            else:
                #TODO change this logic once we stop incremental inventory
                insert_inv_item = self.connect.cursor()
                insert_inv_item.execute("INSERT INTO inventory (item_id) VALUES ('%s')" %(item_id))
                self.connect.commit()
                new_inv_id = insert_inv_item.lastrowid
                insert_inv_item.close()

                inventory_ids.append({
                    'inventory_id': new_inv_id,
                    'lender_id': 0
                    })


        return inventory_ids

    
def getCurrentTimestamp():
    current_timestamp = datetime.datetime.now()
    order_placed = str(current_timestamp).split('.')[0]

    return order_placed


def getDefaultReturnTimestamp():
    current_timestamp = datetime.datetime.now()
    next_week_timestamp = str(current_timestamp + datetime.timedelta(days=7))
    order_return = next_week_timestamp.split('.')[0]

    return order_return

'''
def checkOrderValidity(self):
    check_record_cursor = self.connect.cursor()
    check_record_cursor.execute("SELECT order_id FROM orders WHERE user_id = %d \
            AND item_id = %d AND UNIX_TIMESTAMP(order_return) <= UNIX_TIMESTAMP('%s')" \
            %(self.user, self.item, self.order_placed))
    record_count = check_record_cursor.fetchone()
    check_record_cursor.close()
    return 0 if record_count else 1
'''

