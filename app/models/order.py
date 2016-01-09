from app import mysql
from app import webapp
from app.models import User
from app.models import Item
from app.models import Utils
from app.models import Wallet
from app.models import Mailer
from app.models import Notifications
from datetime import datetime
import json

class Order():
    def __init__(self, order_id):
        self.order_id = order_id

    def getOrderInfo(self, **kwargs):
        # TODO concatnate list of inv_id and item_id when,
        # when going gor mulitple items in same order
        obj_cursor = mysql.connect().cursor()
        obj_cursor.execute("SELECT o.*, oi.* \
                FROM orders o \
                INNER JOIN order_history oi ON o.order_id = oi.order_id \
                WHERE o.order_id = %d" %(self.order_id))
        order_info = Utils.fetchOneAssoc(obj_cursor)
        order_info['item'] = Item(order_info['item_id']).getObj()

        if 'formatted' in kwargs:
            ts = [_ for _ in Order.getTimeSlot() if _['slot_id'] == order_info['pickup_slot']][0]
            order_info['pickup_time'] = Utils.formatTimeSlot(ts)

        return order_info

    @staticmethod
    def placeOrder(order_data):
       
        order_fields = ['item_id', 'user_id', 'address']
        for key in order_fields:
            if key not in order_data.keys():
                return {'message': 'Required params missing'}
            elif not order_data[key]:
                return {'message': 'Wrong param value'}
            else:
                order_data[key] = int(order_data[key]) if key != 'address' else json.loads(order_data[key])
        
        order_data['payment_mode'] = Utils.getParam(order_data, 'payment_mode',
                default = 'cash')
        order_data['order_placed'] = Utils.getCurrentTimestamp()
        order_data['order_return'] = Utils.getParam(order_data, 'order_return', 
                default = Utils.getDefaultReturnTimestamp(order_data['order_placed'], webapp.config['DEFAULT_RETURN_DAYS']))
        order_data['delivery_slot'] = int(Utils.getParam(order_data, 'delivery_slot', 
                default = Utils.getDefaultTimeSlot()))

        #TODO calc total amount
        order_data['order_amount'] = 30 

        #check order validity
        # TODO check if item exists

        # User validity
        user = User(order_data['user_id'], 'user_id')
        user_not_valid = Order.isUserValidForOrder(user, order_data)
        if user_not_valid:
            return user_not_valid

        connect = mysql.connect() 
        insert_data_cursor = connect.cursor()
        insert_data_cursor.execute("""INSERT INTO orders (user_id, 
                address_id, 
                order_placed, 
                order_return, 
                delivery_slot, 
                pickup_slot, 
                payment_mode) 
                VALUES(%d, %d, '%s', '%s', %d, %d, '%s')"""  
                %(order_data['user_id'], 
                    order_data['address']['address_id'], 
                    order_data['order_placed'], 
                    order_data['order_return'], 
                    order_data['delivery_slot'], 
                    order_data['delivery_slot'], 
                    order_data['payment_mode']))
        connect.commit()
        order_id = insert_data_cursor.lastrowid
        insert_data_cursor.close()
        response = {'order_id': order_id}

        order = Order(order_id)
        order.updateInventoryPostOrder([order_data['item_id']])

        if order_data['payment_mode'] == 'wallet':
            Wallet.debitTransaction(user.wallet_id, user.user_id, 'order', order_id, order_data['order_amount']) 

        #TODO call roadrunnr api
        order.sendOrderNotification(1, user)
        Order.notifyAdmin(user.user_id)
        return response 

    @staticmethod
    def notifyAdmin(user_id):
        notification_data = {
                "notification_id":1,
                "title": "ALERT!! Order has been placed",
                }
        admins = [1,5,6,8,9]
        if user_id in admins:
            return
        for u_id in admins:
            user = User(u_id,'user_id')
            Notifications(user.gcm_id).sendNotification(notification_data)
        return True


    def sendOrderNotification(self, status_id, user=None):
        order_info = self.getOrderInfo()
        status_info = self.getOrderStatusDetails(order_info['order_status']) 

        notification_id = 1
        if status_id == 6:
            notification_id = 4
        notification_data = {
                    "notification_id": notification_id,
                    "entity_id": self.order_id,
                    "title": status_info["Status"],
                    "message": status_info["Description"],
                    "expanded_text": status_info["Description"] 
                }

        if user is None:
            user = User(order_info['user_id'], 'user_id')
        Notifications(user.gcm_id).sendNotification(notification_data)


    def updateInventoryPostOrder(self, item_ids):
        # NOTE this part is supported for multiple items in same order. PlaceOrder function isnt

        inventory_ids = self.getInventoryIds(item_ids) 

        #update order_history and clear stock in inventory
        connect = mysql.connect()
        for inventory_item in inventory_ids:
            order_history_cursor = connect.cursor()
            order_history_cursor.execute("INSERT INTO order_history (inventory_id, \
                    item_id, order_id) VALUES (%d, %d, %d)" %(inventory_item['inventory_id'], \
                    inventory_item['item_id'], self.order_id))
            connect.commit()
            order_history_cursor.close()

            update_stock_cursor = connect.cursor()
            update_stock_cursor.execute("UPDATE inventory SET in_stock = 0 WHERE \
                    inventory_id = %d" % (inventory_item['inventory_id']))
            connect.commit()
            update_stock_cursor.close()


    def getInventoryIds(self, item_ids):
        # Incremental Inventory Logic
        #   in_stock: Item is in inventory (not with a user)
        #   fetched: Item has been acquired
        #     
        #   During order, check if acuquired item is in inventory
        #   If not, insert a new item (to be purchased now), which is not yet
        #   bought(thus, fetched=0). 
        #   fetched=1 happens when 
        #   1.status is changed from the dashboard while entering other 
        #     inventory info (price, isbn)
        #   2. Order status changes to 2(en route).(In case the change was not
        #     made form dashboard.

        inventory_ids = []
        for item_id in item_ids:
            item_check_cursor = mysql.connect().cursor()
            item_check_cursor.execute("""SELECT inventory_id FROM
                    inventory WHERE item_id = %d AND in_stock = 1 
                    AND fetched = 1""" % (item_id))
            inv_items = item_check_cursor.fetchall()
            item_check_cursor.close()

            if inv_items: 
                inventory_ids.append({
                    'inventory_id': item_selected[0],
                    'item_id': item_id
                    })
            else:
                connect = mysql.connect()
                insert_inv_item = connect.cursor()
                insert_inv_item.execute("INSERT INTO inventory (item_id) VALUES ('%s')" %(item_id))
                connect.commit()
                new_inv_id = insert_inv_item.lastrowid
                insert_inv_item.close()

                inventory_ids.append({
                    'inventory_id': new_inv_id,
                    'item_id': item_id
                    })

        return inventory_ids

    @staticmethod
    def isUserValidForOrder(user, order_data):
        if user.getObj() is None:
            return {'message': 'User does not exist'}

        # User can only own 2 book @ a time
        if webapp.config['USER_BOOKS_LIMIT']:
            user_orders = user.getAllOrders()
            if (len(user_orders['ordered']) + len(user_orders['reading'])) >= 2:
                #Mailer.excessOrder(user.user_id, order_data['item_id'])
                return {'message': 'Already rented maximum books. We\'ll contact you shortly.'}

        # Wallet validity 
        if order_data['payment_mode'] == 'wallet' and user.wallet_balance is not None and user.wallet_balance < order_data['order_amount']:
            return {'message': 'Not enough balance in wallet'}

        # Since Address is editable before placing order
        if not user.validateUserAddress(order_data['address']):
            return {'message': 'Address not associated'}

        return None


    def getOrderStatusForUser(self, user_id):
        get_status_cursor = mysql.connect().cursor()
        get_status_cursor.execute("SELECT o.order_status, i.item_id FROM orders o \
                INNER JOIN order_history i \
                ON o.order_id = i.order_id \
                WHERE o.order_id = %d \
                AND o.user_id = %d" 
                % (self.order_id, user_id))

        status = get_status_cursor.fetchone()
        if status:
            status_id = int(status[0])
        else:
            return False

        order_info = {}
        if status_id:
            order_info['status_details'] = Order.getOrderStatusDetails(status_id)
            order_info['item'] = Item(int(status[1])).getObj()

        return order_info

   
    @staticmethod    
    def getTimeSlot():
        time_slot_cursor = mysql.connect().cursor()
        time_slot_cursor.execute("SELECT * FROM time_slots")
        num_slots = time_slot_cursor.rowcount

        time_slots = []
        for slot in range(num_slots):
            time_slots.append(Utils.fetchOneAssoc(time_slot_cursor))

        time_slot_cursor.close()
        return time_slots

    def updateOrderStatus(self, status_id):
        conn = mysql.connect()
        update_cursor = conn.cursor()
        update_cursor.execute("UPDATE orders SET order_status = %d WHERE order_id = %d"
                %(status_id, self.order_id))
        conn.commit()

        update_inv_query = ''
        # Putting item back in stock
        if status_id == 7:
            update_inv_query = """UPDATE inventory SET in_stock = 1 WHERE 
                    inventory_id IN (SELECT inventory_id FROM order_history WHERE
                    order_id = %d)""" % (self.order_id)
        elif status_id == 2:
            update_inv_query = """UPDATE inventory SET fetched = 1 WHERE
                    inventory_id IN (SELECT inventory_id FROM order_history WHERE
                    order_id = %d)""" % (self.order_id)

        if update_inv_query:
            update_cursor.execute(update_inv_query) 
            conn.commit()
        update_cursor.close()
        if status_id in [3, 4, 5, 6]:
            self.sendOrderNotification(status_id) 
        return self.getOrderInfo() 

    def editOrderDetails(self, order_data):
        # order_return validity
        order_info = self.getOrderInfo()
        if not order_info:
            return False

        if 'order_return' in order_data:
            old_order_return = datetime.strptime(order_info['order_return'], "%Y-%m-%d %H:%M:%S")
            new_order_return = datetime.strptime(order_data['order_return'], "%Y-%m-%d %H:%M:%S")
            diff = old_order_return - new_order_return 
            if diff.days <= 0:
                return False
        else:
            order_data['order_return'] = order_info['order_return']
       
        if 'pickup_slot' in order_data:
            if not order_data['pickup_slot'].isdigit():
                return False
            else:
                order_data['pickup_slot'] = int(order_data['pickup_slot'])
                slot_exists = False
                for slot in Order.getTimeSlot():
                    if slot['slot_id'] == order_data['pickup_slot']:
                        slot_exists = True
                        break
                if not slot_exists:
                    return False
        else:
            order_data['pickup_slot'] = order_info['pickup_slot']
       
        # NOTE Future generic incomplete code. Remove else part when using this
        '''
        edit_query_string = []
        for data in order_data.keys():
            if data != 'order_id':
                format_value = "'%s'" if isinstance(order_data[data], 'str') else "%d"
                edit_query_string.append(data+" = "+format_value)
        if not edit_query_string:
            return False
        else:
            edit_query_string ", ".join(edit_query_string)
        '''

        conn = mysql.connect()
        update_cursor = conn.cursor()
        update_cursor.execute("""UPDATE orders SET order_return = '%s',
                pickup_slot = %d WHERE
                order_id = %d""" %(order_data['order_return'],
                order_data['pickup_slot'], self.order_id))
        conn.commit()
        if update_cursor.rowcount:
            return True
        else:
            return False


    @staticmethod
    def getTimeSlotsForOrder():
        next_timeslotid = Utils.getDefaultTimeSlot()
        all_timeslots = Order.getTimeSlot()
        for ts in all_timeslots:
            if ts['slot_id'] == next_timeslotid:
                next_timeslot = ts
                break
        order_timeslots = [next_timeslot] + Utils.getNextTimeslots(next_timeslot['start_time'], all_timeslots, 2)

        # Mark day
        # Get day of first time slot and the rest will follow suit
        for i,ts in enumerate(order_timeslots):
            if i == 0:
                if int(ts['start_time'].split(":")[0]) - int(datetime.now().hour) > 0:
                    start_day = 'Today'
                else:
                    start_day = 'Tomorrow'
                day = start_day
            else:
                if int(ts['start_time'].split(":")[0]) - int(next_timeslot['start_time'].split(":")[0]) >= 0:
                    day = start_day
                else:
                    day = 'Tomorrow'

            #Format Timeslots
            formatted_time = Utils.formatTimeSlot(ts)
            ts['formatted'] = day+' '+formatted_time
        return order_timeslots

    @staticmethod
    def getOrderStatusDetails(status_id):
        status_info = {
                1: {
                    "Status": "Order placed",
                    "Description": "Your order has been confirmed"
                    },
                2: {
                    "Status": "Picked up",
                    "Description": "Your order has been picked up for delivery"
                    },
                3: {
                    "Status": "Out for Delivery",
                    "Description": "Your order is on the way"
                    },
                4: {
                    "Status": "Delivered",
                    "Description": "Your order has been delivered"
                    },
                5: {
                    "Status": "Out for pickup",
                    "Description": "We're on our way to pickup the book"
                    },
                6: {
                    "Status": "Picked up",
                    "Description": "Thank you for ordering with us. We hope you enjoyed your book."
                    },
                7: {
                    "Status": "Returned",
                    "Description": "Order has been retured to the inventory"
                    }
                }
        
        if status_id in status_info:
            return status_info[status_id]
        else:
            return False

    
    @staticmethod
    def deleteOrder(order_id):
        conn = mysql.connect()
        delete_cursor = conn.cursor()
        
        order_info = Order(order_id).getOrderInfo()
        if order_info is None:
            return {'status':'false'}

        delete_cursor.execute("""SELECT inventory_id FROM order_history WHERE
        order_id = %d""" %(order_id))
        inventory_id = delete_cursor.fetchone()[0]

        delete_cursor.execute("""DELETE FROM inventory WHERE inventory_id =
        """+ str(inventory_id) +""" AND fetched = 0""") 
        conn.commit()
        
        delete_cursor.execute("DELETE orders, order_history FROM orders INNER JOIN \
        order_history WHERE orders.order_id = order_history.order_id AND orders.order_id = %d"
        %(order_id))
        conn.commit()
        delete_cursor.close()
        return {'status':'true'}

