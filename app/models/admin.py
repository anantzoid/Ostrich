from app import mysql
from app import webapp
from app.models import *
from app.scripts import Indexer
import urlparse
import requests
import time
import re
import os
import json
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from pymongo import MongoClient
from bson import ObjectId

class Admin():
    @staticmethod
    def getCurrentRentals(returns=False):
        rental_list = []
        cursor = mysql.connect().cursor()
        date = "'"+Utils.getCurrentTimestamp().split(' ')[0]+"'"
        query_condition = 'l.status_id >= 4 AND l.status_id < 6 ORDER BY l.delivery_date ASC' if returns else 'l.status_id < 4'
        cursor.execute("""SELECT l.lender_id,
            u.name, u.phone,
            ua.address,
            i.item_id, i.item_name, i.author,
            l.status_id, l.pickup_date, l.pickup_slot,
            l.delivery_date, l.delivery_slot, l.order_placed,
            iv.inventory_id, u.email,
            ua.description, ua.locality, ua.landmark
            FROM lenders l
            INNER JOIN users u ON l.user_id = u.user_id
            INNER JOIN user_addresses ua ON ua.address_id = l.address_id
            INNER JOIN inventory iv ON iv.inventory_id = l.inventory_id
            INNER JOIN items i ON i.item_id = iv.item_id
            WHERE """+query_condition)
        raw_data = cursor.fetchall()
        rental_list = []
        all_time_slots = Order.getTimeSlot()
        for row in raw_data:
            rental = {}
            rental['order_id'] = row[0]
            rental['user'] = {
                    'name': row[1],
                    'phone': row[2],
                    'email': row[14]
                    }
            rental['address'] = {
                    'address': row[3],
                    'description': row[15],
                    'locality': row[16],
                    'landmark': row[17]
                    }
            rental['item'] = {
                    'item_id': row[4],
                    'item_name': row[5],
                    'author': row[6]
                    }
            next_order_status = int(row[7])+1
            rental['change_status'] = {
                    'status_id': next_order_status, 
                    'status': Lend.getLendStatusDetails(next_order_status)['Status']
                    }
            rental['order_status'] = Lend.getLendStatusDetails(row[7])['Status']
            rental['pickup_date'] = str(row[8]) 
            rental['pickup_slot'] = [ts for ts in all_time_slots if ts['slot_id'] == row[9]][0]
            rental['delivery_date'] = str(row[10])
            rental['delivery_slot'] = [ts for ts in all_time_slots if ts['slot_id'] == row[11]][0]
            rental['order_placed'] = str(row[12]) 
            rental['inventory_id'] = row[13]
            rental_list.append(rental)
        return rental_list

    @staticmethod
    def getCurrentOrders(pickups=False):
        order_list = []
        cursor = mysql.connect().cursor()
        date = "'"+Utils.getCurrentTimestamp().split(' ')[0]+"'"
        query_condition = 'order_status >= 4 AND order_status < 7 AND DATE(order_return) >= '+date+' ORDER BY order_return ASC' if pickups else 'order_status < 4'
        cursor.execute("""SELECT order_id FROM orders WHERE """+query_condition)
        order_ids = cursor.fetchall()
        all_time_slots = Order.getTimeSlot()

        for order_id in order_ids:
            order = Order(int(order_id[0]))
            order_info = order.getOrderInfo()

            user = User(order_info['user_id'])
            order_info['user'] = user.getObj()
            order_info['address'] = user.getAddressInfo(order_info['address_id']) 
            order_info['delivery_slot'] = [ts for ts in all_time_slots if ts['slot_id'] == order_info['delivery_slot']][0]
            order_info['pickup_slot'] = [ts for ts in all_time_slots if ts['slot_id'] == order_info['pickup_slot']][0]

            next_order_status = int(order_info['order_status'])+1
            order_info['change_status'] = {
                    'status_id': next_order_status, 
                    'status': Order.getOrderStatusDetails(next_order_status)['Status']
                    }
            order_info['order_status'] = Order.getOrderStatusDetails(order_info['order_status'])['Status']

            # check if item is in inventory
            cursor.execute("""SELECT isbn_13 FROM inventory WHERE inventory_id = %d"""%(order_info['inventory_id']))
            isbn = cursor.fetchone()
            if isbn:
                order_info['isbn_13'] = isbn[0]

            # check for order extensions
            if pickups:
                cursor.execute("""SELECT * FROM edit_order_log WHERE order_id = %s""",(order_id,))
                order_log = cursor.fetchall()
                if order_log:
                    order_info['edit'] = {}
                    for log in order_log:
                        if log[1] == 'order_return':
                            order_info['edit']['old_order_return'] = log[2]
                        elif log[1] == 'charge':
                            if 'charge' not in order_info['edit']:
                                order_info['edit']['charge'] = 0
                            order_info['edit']['charge'] += int(log[3])

            order_list.append(order_info)

        return order_list

    @staticmethod
    def getPickups():
        orders_list = Admin.getCurrentOrders(pickups=True)
        for i,order in enumerate(orders_list):
            orders_list[i]['order_type'] = 'borrow'
            orders_list[i]['scheduled_date'] = order['order_return']
            orders_list[i]['scheduled_slot'] = order['pickup_slot']
        
        rental_list = Admin.getCurrentRentals(returns=True)
        for i,rental in enumerate(rental_list):
            rental_list[i]['order_type'] = 'lend'
            rental_list[i]['scheduled_date'] = rental['delivery_date']
            rental_list[i]['scheduled_slot'] = rental['delivery_slot']
            
        return orders_list+rental_list

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

    @staticmethod
    def insertItem(data):        
        conn = mysql.connect()
        cursor = conn.cursor()
    
        price = data['amazon']['offer_price'] if data['amazon']['offer_price'] else data['amazon']['list_price']
        price = re.sub('\..*$', '', price)

        cursor.execute("""SELECT item_id FROM items WHERE item_name LIKE %s AND author LIKE %s""", (data['amazon']['title'], data['goodreads']['author']))
        match = cursor.fetchone()
        if match:
            return int(match[0])
        cursor.execute("""INSERT INTO items (item_name, price, author, ratings,
        num_ratings, num_reviews, language) VALUES
        (%s,%s,%s,%s,%s,%s,%s)""",
        (data['amazon']['title'],
        price,
        data['goodreads']['author'],
        data['goodreads']['avg_rating'].replace(' rating',''),
        data['goodreads']['num_ratings'],
        data['goodreads']['num_review'],
        data['goodreads']['language']
        ))
        conn.commit()
        item_id = cursor.lastrowid

        cursor.execute("""INSERT INTO item_isbn (item_id, isbn_10,isbn_13, 
        num_pages, binding_type) VALUES 
        (%s,%s,%s,%s,%s)""",
        (item_id,
            data['amazon']['isbn_10'],
            data['amazon']['isbn_13'],
            data['goodreads']['num_page'],
            data['goodreads']['bind_type']))
        conn.commit()
        
        for isbn in data['goodreads']['isbns']:
            cursor.execute("""INSERT INTO item_isbn (item_id, isbn_13) VALUES (%s, %s)""",
                (item_id, isbn))
            conn.commit()

        global_categories = {}
        for genres in data['goodreads']['genres']:
            for genre in genres[0].split(","):
                if genre not in global_categories:
                    cursor.execute("""SELECT category_id FROM categories WHERE category_name = %s""",(genre,))
                    cat_id = cursor.fetchone()
                    if cat_id:
                        global_categories[genre] = cat_id[0]
                        cursor.execute("""INSERT INTO items_categories (item_id, category_id)
                        VALUES (%s, %s)""",(item_id, global_categories[genre]))
                    #TODO insert category if not exists
                conn.commit()

        s3conn = S3Connection('AKIAIN4EU63OJMW63H6A', 'k97pZ8rmwkqLdeW+L4QOIKrCDIg3YR/uY/BifLU3')
        bucket = s3conn.get_bucket('ostrich-catalog')
        basepath = webapp.config['S3_IMAGE_BUCKET']

        url = data['amazon']['img_small']
        parsed = urlparse.urlparse(url)
        ext =  os.path.splitext(parsed.path)[1]
        path = basepath + str(item_id) + ext

        if url:
            r = requests.get(url)
            if r.status_code >= 200 and r.status_code <300:
                content = r.content
                key = Key(bucket)
                key.key = path
                key.set_contents_from_string(content)

                cursor.execute("""UPDATE items SET img_small = %s WHERE item_id = %s""",
                        (path, item_id))
                conn.commit()

        Indexer().indexItems(query_condition=' AND i.item_id='+str(item_id))
    
        client =  MongoClient(webapp.config['MONGO_DB'])
        db = client.ostrich
        final_data = data['goodreads']
        final_data.update(data['amazon'])
        final_data['_id'] = int(item_id)
        if not db.items.find({'_id': final_data['_id']}).count():
            db.items.insert_one(final_data)

        return final_data

    @staticmethod
    def savePanelData(data):
        client =  MongoClient(webapp.config['MONGO_DB'])
        db = client.ostrich
        panel_data = {
            'title': data['title'],
            'items': data['items'].split(',') 
        }
        print db.content.update_one(
                {'_id': ObjectId(data['_id'])},
                {'$set': panel_data}
                )
        return True

    @staticmethod
    def getSearchFailedQueries():
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT * FROM search_fails WHERE flow != 'admin' AND item_id IS NULL 
                ORDER BY timestamp DESC""")
        numrows = cursor.rowcount
        data = []
        for i in range(numrows):
            data.append(Utils.fetchOneAssoc(cursor))
        return data
    
    @staticmethod
    def submitSearchFailItem(args):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""UPDATE search_fails SET item_id = %s WHERE id = %s""",
                (args['item_id'], args['query_id']))
        conn.commit()
        return True

    @staticmethod
    def sendSearchFailNotification(data):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM search_fails WHERE id = %s""",(data['query_id'],))
        search_data = cursor.fetchone()
        if not search_data[6]:
            return
        if search_data[1] <= 0:
            return
        
        item = Item(int(search_data[6]))
        user = User(int(search_data[1]))

        item_name_ellipse = (order_info['item']['item_name'][:27] + '..') if len(order_info['item']['item_name']) > 27 else order_info['item']['item_name'] 
        notif_msg = "We have noticed you were searching for "+item_name_ellipse+" but didn't get the expected results. We've added the book for you. Tap here to open it up."
        notification_data = {
                "notification_id": 5,
                "entity_id": item.item_id,
                "item_name": item.item_name,
                "search_intention": search_data[5],
                "title": item_name+" is now available",
                "message": notif_msg, 
                "expanded_text": notif_msg
                }
        status = Notifications(user.gcm_id).sendNotification(notification_data) 
        if status and 'success' in status:
            cursor.execute("""UPDATE search_fails SET gcm_token = %s WHERE id = %s""", (json.dumps(status['success']), data['query_id']))
            conn.commit()
        return True
