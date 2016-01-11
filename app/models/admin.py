from app import mysql
from app.models import *

class Admin():
    @staticmethod
    def getCurrentRentals():
        rental_list = []
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT l.lender_id,
            u.name, u.phone,
            ua.address,
            i.item_id, i.item_name, i.author,
            l.status_id, l.pickup_date, l.pickup_slot,
            iv.inventory_id
            FROM lenders l
            INNER JOIN users u ON l.user_id = u.user_id
            INNER JOIN user_addresses ua ON ua.address_id = l.address_id
            INNER JOIN inventory iv ON iv.inventory_id = l.inventory_id
            INNER JOIN items i ON i.item_id = iv.item_id
            WHERE l.status_id < 4""")
        raw_data = cursor.fetchall()
        rental_list = []
        all_time_slots = Order.getTimeSlot()
        for row in raw_data:
            rental = {}
            rental['order_id'] = row[0]
            rental['user'] = {
                    'name': row[1],
                    'phone': row[2]
                    }
            rental['address'] = {'address': row[3]}
            rental['item'] = {
                    'item_id': row[4],
                    'item_name': row[5],
                    'author': row[6]
                    }
            rental['order_placed'] = row[8] 
            next_order_status = int(row[7])+1
            rental['change_status'] = {
                    'status_id': next_order_status, 
                    'status': Lend.getLendStatusDetails(next_order_status)['Status']
                    }
            rental['order_status'] = Lend.getLendStatusDetails(row[7])['Status']
            rental['delivery_slot'] = [ts for ts in all_time_slots if ts['slot_id'] == row[9]][0]
            rental['inventory_id'] = row[10]
            rental_list.append(rental)
        return rental_list

    @staticmethod
    def getCurrentOrders():
        order_list = []
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT order_id FROM orders WHERE order_status < 4""")
        order_ids = cursor.fetchall()
        all_time_slots = Order.getTimeSlot()

        for order_id in order_ids:
            order = Order(int(order_id[0]))
            order_info = order.getOrderInfo()

            user = User(order_info['user_id'])
            order_info['user'] = user.getObj()
            order_info['address'] = user.getUserAddress(order_info['address_id']) 

            order_info['delivery_slot'] = [ts for ts in all_time_slots if ts['slot_id'] == order_info['delivery_slot']][0]
            next_order_status = int(order_info['order_status'])+1
            order_info['change_status'] = {
                    'status_id': next_order_status, 
                    'status': Order.getOrderStatusDetails(next_order_status)['Status']
                    }
            order_info['order_status'] = Order.getOrderStatusDetails(order_info['order_status'])['Status']

            # check if item is in inventory
            cursor.execute("""SELECT isbn_13 FROM inventory WHERE inventory_id = %d"""%(order_info['inventory_id']))
            order_info['isbn_13'] = cursor.fetchone()[0]
            order_list.append(order_info)

        return order_list

    @staticmethod
    def getItemDetail(inventory_id):
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT iv.price, iv.item_condition, iv.source, ii.*
            FROM inventory iv 
            LEFT JOIN item_isbn ii ON ii.isbn_13 = iv.isbn_13
            WHERE iv.inventory_id = %d""" %(inventory_id))
        inv_data = Utils.fetchOneAssoc(cursor)
        cursor.close()
        return inv_data

    @staticmethod
    def setInventoryData(inv_data):
        '''
            ISBN 13 would exist in inventory if item exists. Also item_isbn would
            have corresponding details. Thus update item_isbn with changed details.

            If not updated, update inventory with isbn and insert in item_isbn
        '''
        inv_insert_data = {}
        for key in inv_data.keys():
            inv_insert_data[key] = None if inv_data[key] in ['null',''] else inv_data[key]
            if key in ['item_id', 'num_pages', 'inventory_id']:
                if inv_insert_data[key] is None:
                    inv_insert_data[key] = 0
                else:
                    inv_insert_data[key] = float(inv_insert_data[key])

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""UPDATE item_isbn SET 
            isbn_10=%s, 
            publisher=%s,
            publication_year=%s,
            dimensions=%s,
            num_pages=%s,
            binding_type=%s
            WHERE isbn_13 = %s""",
        (inv_insert_data['isbn_10'], inv_insert_data['publisher'], inv_insert_data['publication_year'],
        inv_insert_data['dimensions'], inv_insert_data['num_pages'], inv_insert_data['binding_type'], inv_insert_data['isbn_13']))
        conn.commit()
        affected = cursor.rowcount

        if not affected:
            cursor.execute("""INSERT INTO item_isbn (item_id, isbn_10, isbn_13,
                publisher, publication_year, num_pages, dimensions, binding_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (inv_insert_data['item_id'], inv_insert_data['isbn_10'], 
                inv_insert_data['isbn_13'],
                inv_insert_data['publisher'], inv_insert_data['publication_year'],
                inv_insert_data['num_pages'], inv_insert_data['dimensions'], 
                inv_insert_data['binding_type']))

            conn.commit()
        cursor.execute("""UPDATE inventory SET isbn_13 = %s, price = %s, item_condition = %s, source = %s
                WHERE inventory_id = %s""",
                (inv_insert_data['isbn_13'], inv_insert_data['price'], 
                inv_insert_data['item_condition'], inv_insert_data['source'], inv_insert_data['inventory_id']))
        conn.commit() 
        return True            

