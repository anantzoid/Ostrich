from app import webapp
from app import mysql
from app.models import *
from app.scripts import Indexer
import json


class Lend():
    @staticmethod
    def getOfferCredits():
        return int(3 * webapp.config['NEW_READING_RATE'] * webapp.config['DEFAULT_RETURN_DAYS'])

    @staticmethod
    def lendItem(lend_data):
        lend_fields = ['item_id', 'user_id', 'address']
        for key in lend_fields:
            if key not in lend_data.keys():
                return {'message': 'Required params missing'}
            elif not lend_data[key]:
                return {'message': 'Wrong param value'}
            else:
                lend_data[key] = int(lend_data[key]) if key != 'address' else json.loads(lend_data[key])

        lend_data['pickup_date'] = Utils.getParam(lend_data, 'pickup_date',
                default=Utils.getCurrentTimestamp())
        lend_data['delivery_date'] = Utils.getParam(lend_data,'delivery_date', 
                default=Utils.getDefaultReturnTimestamp(lend_data['pickup_date'], 45))
        lend_data['pickup_slot'] = int(Utils.getParam(lend_data, 'pickup_slot',
               default = Utils.getDefaultTimeSlot()))
        lend_data['delivery_slot'] = lend_data['pickup_slot']

        # Item conditions is a list of {"name":"condition", "selected": "True/False"}
        item_conditions = Utils.getParam(lend_data, 'item_condition', default=None)
        if item_conditions is not None:
            item_conditions = json.loads(item_conditions)
        else:
            item_conditions = [{'name':'New', 'selected':'true'}]
        lend_data['item_condition'] = []
        for condition in item_conditions:
            if condition['selected'].lower() == "true":
                lend_data['item_condition'].append(condition['name'])
        lend_data['item_condition'] = "|".join(lend_data['item_condition'])

        # Since Address is editable before placing order
        user = User(lend_data['user_id'], 'user_id')
        if not user.validateUserAddress(lend_data['address']):
            return {'message': 'Address not associated'}
        if not Lend.isUserValidForLending(lend_data):
            return ({
                'title': 'Cannot Offer a Borrowed Book',
                'message': 'You cannot offer a book borrowed with Ostrich. Please try again with another book.'},
                'HTTP_STATUS_CODE_CLIENT_ERROR')

        conn = mysql.connect()
        set_lend_cursor = conn.cursor()
       
        set_lend_cursor.execute("""INSERT INTO inventory (item_id, 
                date_added, date_removed, item_condition) VALUES 
                (%d, '%s', '%s', '%s')""" % 
                (lend_data['item_id'], 
                 str(lend_data['pickup_date']), 
                 str(lend_data['delivery_date']), 
                 lend_data['item_condition'] 
                ))
        conn.commit()
        lend_data['inventory_id'] = set_lend_cursor.lastrowid
        set_lend_cursor.close()

        lend_data['lender_id'] = Lend.addLender(lend_data) 
        if not lend_data['lender_id']:
            Lend.rollbackLend(lend_data['inventory_id'])
            return {}

        Wallet.creditTransaction(user.wallet_id, user.user_id, 'lend', 
                lend_data['inventory_id'], Lend.getOfferCredits()) 
       
        Lend.sendLendNotification(status_id=1,user=user)
        Utils.notifyAdmin(user.user_id, 'Lend')
        return {'inventory_id': lend_data['inventory_id'], 'lender_id':
                lend_data['lender_id']}

    @staticmethod
    def isUserValidForLending(lend_data):
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT COUNT(*) FROM orders o
            INNER JOIN order_history oh ON oh.order_id = o.order_id
            WHERE oh.item_id = %s AND
            o.user_id = %s AND o.order_status < 7""", 
            (lend_data['item_id'], lend_data['user_id']))  
        exists = cursor.fetchone()[0]
        if exists:
            return False
        return True

    @staticmethod    
    def addLender(lend_data):
        conn = mysql.connect()
        lender_cusror = conn.cursor()
        lender_cusror.execute("""INSERT into lenders (
            inventory_id,
            user_id,
            delivery_date,
            pickup_date,
            delivery_slot,
            pickup_slot,
            address_id) VALUES (%d, %d, '%s', '%s', %d, %d, %d) """
            %(lend_data['inventory_id'],
                lend_data['user_id'],
                lend_data['delivery_date'],
                lend_data['pickup_date'],
                lend_data['delivery_slot'],
                lend_data['pickup_slot'],
                lend_data['address']['address_id']))
        conn.commit()
        lender_id = lender_cusror.lastrowid
        lender_cusror.close()
        return lender_id


    @staticmethod    
    def rollbackLend(inventory_id):
        conn = mysql.connect()
        del_cursor = conn.cursor()
        del_cursor.execute("""DELETE FROM inventory WHERE inventory_id = %d"""
                %(inventory_id))
        conn.commit()
        return True

    @staticmethod
    def updateLendStatus(lender_id, status_id):
        if not Lend.getLendStatusDetails(status_id):
            return False

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""UPDATE lenders SET status_id = %d WHERE lender_id = %d"""
                %(status_id, lender_id))
        conn.commit()

        if status_id in [1,2,3]:
            cursor.execute("""SELECT l.inventory_id, l.user_id, iv.item_id 
                FROM lenders l 
                INNER JOIN inventory iv ON iv.inventory_id = l.inventory_id
                WHERE l.lender_id = %s""",(lender_id,))
            data = cursor.fetchone()
            user = User(data[1])
            Lend.sendLendNotification(lender_id, status_id, user)

            if status_id == 3:
                cursor.execute("""UPDATE inventory SET in_stock = 1, fetched = 1 WHERE
                inventory_id = %s""",(data[0],))
                conn.commit()
                Indexer().indexItems(query_condition=' AND i.item_id='+str(data[2]))
                Mailer.thankyou(user)


        '''
        NOTE Later
        if status_id == 5:
            cursor.execute("""UPDATE inventory SET in_stock = 0 WHERE
            inventory_id = (SELECT inventory_id FROM lenders WHERE lender_id = %d)"""
            %(lender_id))
            conn.commit()
        '''

        return True

    @staticmethod
    def sendLendNotification(lender_id=0, status_id=0, user=None):
        if user is None and not lender_id:
            return

        if user is None:
            cursor = mysql.connect().cursor()
            cursor.execute("""SELECT user_id FROM lenders WHERE lender_id = %d"""
                    %(lender_id))
            user_id = cursor.fetchone()
            if not user_id:
                return
            user_id = int(user_id[0])
            user = User(user_id, 'user_id')

        status_info = Lend.getLendStatusDetails(status_id)

        notification_id = 1
        if status_id == 6:
            notification_id = 4

        notification_data = {
                "notification_id": notification_id,
                "entity_id": lender_id,
                "title": status_info["Status"],
                "message": status_info["Description"],
                "expanded_text": status_info["Description"] if "expanded_text" not in status_info else status_info["expanded_text"]
                }
        Notifications(user.gcm_id).sendNotification(notification_data)
        return 

    @staticmethod
    def getLendStatusDetails(status_id):
        # NOTE 5,6 are not used now as book is not returned
        status_info = {
                1: {
                    "Status": "Request Received",
                    "Description": "Your request has been received successfully",
                    "expanded_text" : "Your request to offer the book has been received successfully."
                    },
                2: {
                    "Status": "Out for Pickup",
                    "Description": "We're on our way to pick up the book."
                    },
                3: {
                    "Status": "Thanks for Sharing",
                    "Description": "Your book can mean a world to someone."
                    },
                4: {
                    "Status": "Delivered",
                    "Description": "Order has been reported to inventory."
                    },
                5: {
                    "Status": "Out for Pickup",
                    "Description": "Your book is on the way back to you."
                    },
                6: {
                    "Status": "Returned",
                    "Description": "Thanks for sharing your book.",
                    "expanded_text": "Thanks for sharing your book. Your book can mean a world to someone.",
                    }
                }

        if status_id in status_info:
            return status_info[status_id]
        else: 
            return False

    

    @staticmethod
    def deleteRental(lender_id):
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("""SELECT user_id, inventory_id FROM lenders WHERE lender_id= %s""",
        (lender_id,))
        (user_id, inventory_id) = cursor.fetchone()
        if not user_id:
            return {'status':'false'}

        cursor.execute("""DELETE FROM inventory WHERE inventory_id = %s""",
        (inventory_id,))
        conn.commit()

        cursor.execute("""DELETE FROM lenders WHERE lender_id = %s""", (lender_id,))
        conn.commit()

        user = User(user_id) 
        Wallet.debitTransaction(user.wallet_id, user.user_id, 'cancellation', lender_id, Lend.getOfferCredits())
        
        return {'status':'true'}
        
