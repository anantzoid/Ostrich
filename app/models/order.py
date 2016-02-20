from app import mysql
from app import webapp
from app.models import *
from app.scripts import Indexer
import datetime
from app.decorators import async
import json
import pytz

class Order():
    def __init__(self, order_id):
        self.order_id = order_id

    def getOrderInfo(self, **kwargs):
        # TODO concatnate list of inv_id and item_id when,
        # when going gor mulitple items in same order
        obj_cursor = mysql.connect().cursor()
        obj_cursor.execute("""SELECT o.*, oi.*,
                IF((select count(*) from orders where parent_id=%s)>0, 1, 0) as is_parent
                FROM orders o 
                INNER JOIN order_history oi ON o.order_id = oi.order_id 
                WHERE o.order_id = %s""", (self.order_id, self.order_id))
        order_info = Utils.fetchOneAssoc(obj_cursor)
        obj_cursor.close()

        if order_info:
            order_info['item'] = Item(order_info['item_id']).getObj()
            order_info['all_charges'] = [{
                                'charge': int(webapp.config['DEFAULT_RETURN_DAYS'] * webapp.config['NEW_READING_RATE']), 
                                'payment_mode': order_info['payment_mode']}]

            if 'formatted' in kwargs:
                order_info['pickup_time'] = Utils.cleanTimeSlot(Order.getTimeSlot(order_info['pickup_slot']))
            
            if order_info['parent_id'] or order_info['is_parent']:
                if 'fetch_all' in kwargs:
                    fetch_all = kwargs['fetch_all']
                else:
                    fetch_all = False
                order_info = Order.clubOrders(order_info, fetch_all)

        return order_info

    @staticmethod
    def clubOrders(order_info, fetch_all=False):
        parents, children = [], []
        charge = 0
        if order_info['parent_id']:
            parents = Order.getAllParents(order_info, parents)
        if order_info['is_parent']:
            children = Order.getAllChildren(order_info, children)

        if parents:
            order_info['order_placed'] = parents[-1]['order_placed']
        if children:
            order_info['order_return'] = children[-1]['order_return']
            order_info['pickup_slot'] = children[-1]['pickup_slot']
            order_info['order_id'] = children[-1]['order_id']

        all_orders = parents + children
        for order in all_orders:
            charge += order['charge']
            order_info['all_charges'].append({
                    'charge': order['charge'],
                    'payment_mode': order['payment_mode']
                    })
        order_info['charge'] += charge
    
        if fetch_all:
            return {'parents':parents, 'order': order_info, 'children': children}

        return order_info

    @staticmethod
    def getAllParents(order_info, parents):
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT * FROM orders WHERE order_id = %s""",(order_info['parent_id'],))
        parent_data = Utils.fetchOneAssoc(cursor)
        cursor.close()
        parents.append(parent_data)
        if parent_data['parent_id']:
            return Order.getAllParents(parent_data, parents)
        return parents
        
    
    @staticmethod
    def getAllChildren(order_info, children):
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT o.*,
                IF((select count(*) from orders co where co.parent_id=o.order_id)>0, 1, 0) as is_parent
                FROM orders o WHERE o.parent_id = %s""",(order_info['order_id'],))
        child_data = Utils.fetchOneAssoc(cursor)
        cursor.close()
        children.append(child_data)

        if child_data['is_parent']:
            return Order.getAllChildren(child_data, children)
        return children


    @staticmethod
    def placeOrder(order_data):
       
        order_fields = ['item_id', 'user_id']
        for key in order_fields:
            if key not in order_data.keys():
                return {'message': 'Required params missing'}
            elif not order_data[key] or not order_data[key].isdigit():
                return {'message': 'Wrong param value'}
            else:
                order_data[key] = int(order_data[key])
       
        if 'address_id' in order_data:
            order_data['address'] = {}
            order_data['address']['address_id'] = int(order_data['address_id'])
        else:
            order_data['address'] = json.loads(order_data['address'])
            

        order_data['payment_mode'] = Utils.getParam(order_data, 'payment_mode',
                default = 'cash')
        order_data['order_placed'] = Utils.getCurrentTimestamp()
        order_data['delivery_slot'] = int(Utils.getParam(order_data, 'delivery_slot', 
                default = Utils.getDefaultTimeSlot()))
        order_data['delivery_date'] = Utils.getParam(order_data, 'delivery_date', default = order_data['order_placed'])
        order_data['order_return'] = Utils.getParam(order_data, 'order_return', 
                default = Utils.getDefaultReturnTimestamp(order_data['delivery_date'], webapp.config['DEFAULT_RETURN_DAYS']))
        
        #TODO calc total amount
        order_data['order_amount'] = int(webapp.config['DEFAULT_RETURN_DAYS'] * webapp.config['NEW_READING_RATE'])  

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
                delivery_date,
                delivery_slot, 
                pickup_slot, 
                payment_mode) 
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""  
                ,(order_data['user_id'], 
                    order_data['address']['address_id'], 
                    order_data['order_placed'], 
                    order_data['order_return'], 
                    order_data['delivery_date'], 
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

        order.sendOrderNotification(1, user)
        Utils.notifyAdmin(user.user_id, 'Order')
        return response 

    @async
    def sendOrderNotification(self, status_id, user=None):
        order_info = self.getOrderInfo()
        status_info = self.getOrderStatusDetails(order_info['order_status']) 
        
        notification_id = 3
        if status_id == 6:
            notification_id = 4
        if status_id == 1:

            # Notification message formatting
            if len(order_info['item']['item_name']) > 35:
                item_name_ellipse = order_info['item']['item_name'][:35] + '..'
            elif len(order_info['item']['item_name']) + len(order_info['item']['author']) <= 32:
                item_name_ellipse = order_info['item']['item_name'] +' by '+ order_info['item']['author']
            else:
                item_name_ellipse = order_info['item']['item_name']

            status_info["Description"] = status_info["Description"]%item_name_ellipse

            day_today = datetime.datetime.now(pytz.timezone('Asia/Calcutta')).day
            delivery_day = datetime.datetime.strptime(order_info['delivery_date'],"%Y-%m-%d %H:%M:%S")
            if day_today == delivery_day.day:
                day = "Today"
            else:
                day_tomorrow = (datetime.datetime.now(pytz.timezone('Asia/Calcutta'))+datetime.timedelta(days=1)).day
                if day_tomorrow == delivery_day.day:
                    day = "Tomorrow"
                else:
                    day = "on " + delivery_day.strftime("%A")
            status_info["expanded_text"] = status_info["expanded_text"]%(order_info['item']['item_name'], day)

        notification_data = {
                    "notification_id": notification_id,
                    "entity_id": order_info['order_id'],
                    "title": status_info["Status"],
                    "message": status_info["Description"],
                    "expanded_text": status_info["Description"] if "expanded_text" not in status_info else status_info["expanded_text"]
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
            Indexer().indexItems(query_condition=' AND i.item_id='+str(inventory_item['item_id']))
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
                    'inventory_id': inv_items[0][0],
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
        
        # IF the user is already possessing the book
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT COUNT(*) FROM orders o
            INNER JOIN order_history oh ON oh.order_id=o.order_id
            WHERE o.user_id = %s AND  oh.item_id = %s AND o.order_status < 5""",
            (user.user_id, order_data['item_id']))
        if cursor.fetchone()[0]:
            return ({
                'title': 'Book Already Ordered',
                'message': 'It seems you have already ordered this book from Ostrich. Please check the "My Orders" section.'}, 
                'HTTP_STATUS_CODE_CLIENT_ERROR')

        # User can only own 2 book @ a time
        if webapp.config['USER_BOOKS_LIMIT']:
            user_orders = user.getAllOrders()
            if (len(user_orders['ordered']) + len(user_orders['reading'])) >= 2:
                #TODO enable this
                #Mailer.excessOrder(user.user_id, order_data['item_id'])
                return ({
                    'title': 'Order Limit Reached',
                    'message': 'You can keep a maximum of 2 books at a time. Please return a book that you are not reading from the "My Orders" section and try ordering again.'}, 
                    'HTTP_STATUS_CODE_ORDER_LIMIT_EXCEEDED')

        # Wallet validity 
        if order_data['payment_mode'] == 'wallet' and user.wallet_balance < order_data['order_amount']:
            current_balance = str(user.wallet_balance) if user.wallet_balance is not None else "0.0"
            return ({
                'title': 'Not Enough Credits',
                'message': 'Your current balance '+current_balance+' is not enough for this order. Choose the Cash option and please order again.'}, 
                'HTTP_STATUS_CODE_CLIENT_ERROR')

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
    def getTimeSlot(slot_id=None, active=0):
        query_cond = " WHERE active = 1" if active else ""

        time_slot_cursor = mysql.connect().cursor()
        time_slot_cursor.execute("SELECT * FROM time_slots" + query_cond)
        num_slots = time_slot_cursor.rowcount

        time_slots = []
        for slot in range(num_slots):
            time_slots.append(Utils.fetchOneAssoc(time_slot_cursor))

        time_slot_cursor.close()
        if slot_id:
            time_slots = [_ for _ in time_slots if _['slot_id'] == slot_id][0]
        return time_slots

    def updateOrderStatus(self, status_id):
        conn = mysql.connect()
        update_cursor = conn.cursor()
      
        all_orders = self.getOrderInfo(fetch_all=True)
        if 'order' in all_orders:
            all_order_ids = Order.fetchAllOrderIds(all_orders)
        else:
            all_order_ids = str(all_orders['order_id'])

        update_cursor.execute("UPDATE orders SET order_status = %s WHERE order_id IN ("+all_order_ids+")"
                ,(status_id, ))
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
        elif status_id == 7:
            Indexer().indexItems(query_condition=' AND i.item_id='+str(self.getOrderInfo()['item_id']))
        return self.getOrderInfo() 

    def editOrderDetailsNew(self, order_data):
        conn = mysql.connect()
        update_cursor = conn.cursor()

        all_orders = self.getOrderInfo(fetch_all=True)
        if 'order' in all_orders:
            all_order_ids = Order.fetchAllOrderIds(all_orders)
            order_info = all_orders['order']
        else:
            order_info = all_orders
            all_order_ids = str(order_info['order_id'])

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
                update_cursor.execute("""UPDATE orders SET pickup_slot = %s 
                        WHERE order_id IN ("""+all_order_ids+""")""",(order_data['pickup_slot'],))
                conn.commit()
                status = True if update_cursor.rowcount else False

        if 'order_return' in order_data:
            old_order_return = datetime.datetime.strptime(order_info['order_return'], "%Y-%m-%d %H:%M:%S")
            new_order_return = datetime.datetime.strptime(order_data['order_return'], "%Y-%m-%d %H:%M:%S")
            diff = new_order_return - old_order_return
            if diff.days <= 0:
                update_cursor.execute("""UPDATE orders SET order_return = %s
                        WHERE order_id IN ("""+all_order_ids+""")""",(order_data['order_return'],))
                conn.commit()
                status = True if update_cursor.rowcount else False
            else:
                # NOTE Order Extend is a new order
                update_cursor.execute("""INSERT INTO orders 
                    (user_id, 
                    address_id, 
                    order_status,
                    order_return,
                    pickup_slot, 
                    delivery_date,
                    delivery_slot,
                    charge,
                    payment_mode,
                    parent_id) 
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""  
                    ,(order_info['user_id'], 
                    order_info['address_id'], 
                    order_info['order_status'],
                    order_data['order_return'], 
                    order_info['pickup_slot'],
                    order_info['delivery_date'],
                    order_info['delivery_slot'],
                    order_data['extend_charges'] if 'extend_charges' in order_data else order_info['charge'],
                    order_data['extend_payment_mode'] if 'extend_payment_mode' in order_data else 'cash',
                    self.order_id))
                conn.commit()
                child_order_id = update_cursor.lastrowid
                status = True if update_cursor.rowcount else False

                update_cursor.execute("""INSERT INTO order_history 
                    (inventory_id, item_id, order_id) VALUES (%s, %s, %s)""",
                    (order_info['inventory_id'], order_info['item_id'], child_order_id))
                conn.commit()

        self.logEditOrderDetails(order_data, order_info)
        return status

    def editOrderDetails(self, order_data):
        # order_return validity
        order_info = self.getOrderInfo()
        if not order_info:
            return False

        if 'order_return' in order_data:
            ''''
            old_order_return = datetime.datetime.strptime(order_info['order_return'], "%Y-%m-%d %H:%M:%S")
            new_order_return = datetime.datetime.strptime(order_data['order_return'], "%Y-%m-%d %H:%M:%S")
            diff = new_order_return - old_order_return
            #if diff.days <= 0:
            #TODO send notification
            '''
        else:
            order_data['order_return'] = order_info['order_return']
       
        if 'extend_charges' not in order_data:
            order_data['charge'] = order_info['charge']
        else:
            order_data['charge'] = order_data['extend_charges']

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
       
        conn = mysql.connect()
        update_cursor = conn.cursor()
        update_cursor.execute("""UPDATE orders SET order_return = %s,
                pickup_slot = %s, charge = %s WHERE
                order_id = %s""", (order_data['order_return'],
                order_data['pickup_slot'], order_data['charge'], order_info['order_id']))
        conn.commit()
        if update_cursor.rowcount:
            status =  True
        else:
            status =  False

        self.logEditOrderDetails(order_data, order_info)
        return status

    @async
    def logEditOrderDetails(self, order_data, order_info):
        conn = mysql.connect()
        update_cursor = conn.cursor()
        for key in ['order_return', 'pickup_slot', 'charge']:
            if key in order_data and order_data[key] != order_info[key]:
                update_cursor.execute("""INSERT INTO edit_order_log (order_id, 
                `key`, old_value, new_value) VALUES (%s, %s, %s, %s)""",
                (order_info['order_id'], key, str(order_info[key]), str(order_data[key])))
                conn.commit()


    @staticmethod
    def fetchAllOrderIds(all_orders):
        all_order_ids = []
        for key in all_orders.keys():
            value = all_orders[key]
            if isinstance(value, list):
                all_order_ids.extend([_['order_id'] for _ in value])
            else:
                all_order_ids.append(value['order_id'])
        return ",".join([str(_) for _ in all_order_ids])

    @staticmethod
    def getAreasForOrder():
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT * FROM areas WHERE active=1""")
        num_areas = cursor.rowcount
        
        areas = {}
        for area in range(num_areas):
            area_data = Utils.fetchOneAssoc(cursor)
            areas[area_data['name']] = area_data
        return areas

    @staticmethod
    def getTimeSlotsForOrder(interval=6):
        next_timeslotid = Utils.getDefaultTimeSlot(interval)
        all_timeslots = Order.getTimeSlot(active=1)
        for ts in all_timeslots:
            if ts['slot_id'] == next_timeslotid:
                next_timeslot = ts
                break
        order_timeslots = [next_timeslot] + Utils.getNextTimeslots(next_timeslot['start_time'], all_timeslots, 2)
        return Utils.formatTimeSlots(order_timeslots)


    @staticmethod
    def deleteOrder(order_id):
        conn = mysql.connect()
        delete_cursor = conn.cursor()
        
        all_orders = Order(order_id).getOrderInfo(fetch_all=True)
        if 'order' in all_orders:
            all_order_ids = Order.fetchAllOrderIds(all_orders)
            order_info = all_orders['order']
        else:
            order_info = all_orders
            all_order_ids = str(order_info['order_id'])

        if order_info is None:
            return {'status':'false'}


        delete_cursor.execute("""SELECT inventory_id FROM order_history WHERE
        order_id = %d""" %(order_id))
        inventory_id = delete_cursor.fetchone()[0]

        q_cond = """ AND fetched = 1"""

        delete_cursor.execute("""DELETE FROM inventory WHERE inventory_id =
        """+ str(inventory_id) + q_cond) 
        conn.commit()
        
        delete_cursor.execute("DELETE orders, order_history FROM orders INNER JOIN \
        order_history WHERE orders.order_id = order_history.order_id AND orders.order_id IN ("+all_order_ids+")")
        conn.commit()
        delete_cursor.close()
        return {'status':'true'}


    @staticmethod
    def getOrderStatusDetails(status_id):
        status_info = {
                1: {
                    "Status": "Order Placed",
                    "Description": "%s",
                    "expanded_text" : "Your order for the book \"%s\" has been placed successfully. The book will be delivered %s."
                    },
                2: {
                    "Status": "Picked Up",
                    "Description": "Your order has been picked up for delivery."
                    },
                3: {
                    "Status": "Out for Delivery",
                    "Description": "Your book is on its way."
                    },
                4: {
                    "Status": "Book Delivered",
                    "Description": "Enjoy reading your book and don't forget to rate it."
                    },
                5: {
                    "Status": "Out for Pickup",
                    "Description": "We're on our way to pick up the book."
                    },
                6: {
                    "Status": "Book Picked Up",
                    "Description": "Thank you for using Ostrich. We hope you enjoyed your book.",
                    "expanded_text" : "Thank you for using Ostrich. We hope you enjoyed your book. Would you like to order another?"
                    },
                7: {
                    "Status": "Returned",
                    "Description": "Order has been retured to the inventory."
                    }
                }
        
        if status_id in status_info:
            return status_info[status_id]
        else:
            return False
