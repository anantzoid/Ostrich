from app import mysql
from app import webapp
from app.models import *
from app.scripts import Indexer
from app.decorators import async
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
from datetime import datetime
from slugify import slugify

class Admin():
    @staticmethod
    def getCurrentRentals(returns=False):
        rental_list = []
        cursor = mysql.connect().cursor()
        date = "'"+Utils.getCurrentTimestamp().split(' ')[0]+"'"
        query_condition = 'l.status_id >= 4 AND l.status_id < 6' if returns else 'l.status_id < 4'
        query_condition += ' ORDER BY l.delivery_date ASC' 

        cursor.execute("""SELECT l.lender_id,
            u.name, u.phone,
            ua.address,
            i.item_id, i.item_name, i.author,
            l.status_id, l.pickup_date, l.pickup_slot,
            l.delivery_date, l.delivery_slot, l.order_placed,
            iv.inventory_id, u.email,
            ua.description, ua.locality, ua.landmark,
            co.comment, co.edited, co.delivered_by, co.delivery_amount,
            co.picked_by, co.pickup_amount
            FROM lenders l
            INNER JOIN users u ON l.user_id = u.user_id
            INNER JOIN user_addresses ua ON ua.address_id = l.address_id
            INNER JOIN inventory iv ON iv.inventory_id = l.inventory_id
            INNER JOIN items i ON i.item_id = iv.item_id
            LEFT JOIN orders_admin_notes co ON co.order_id = l.lender_id AND co.order_type = 'lend' 
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
            rental['comment'] = row[18]
            rental['edited'] = row[19]
            rental['delivered_by'] = row[20]
            rental['delivery_amount'] = row[21]
            rental['picked_by'] = row[22]
            rental['pickup_amount'] = row[23]
            rental_list.append(rental)
        return rental_list

    @staticmethod
    def getCurrentOrders(pickups=False):
        order_list = []
        cursor = mysql.connect().cursor()
        date = "'"+Utils.getCurrentTimestamp().split(' ')[0]+"'"
        query_condition = 'order_status >= 4 AND order_status < 7' if pickups else 'order_status < 4'
        query_condition += '  ORDER BY order_id ASC' 
        cursor.execute("""SELECT o.order_id,
                co.comment, co.edited, co.delivered_by, co.delivery_amount,
                co.picked_by, co.pickup_amount
                FROM orders o 
                LEFT JOIN orders_admin_notes co ON co.order_id = o.order_id AND co.order_type = 'borrow' 
                WHERE o.order_id NOT IN (SELECT DISTINCT parent_id FROM orders) AND """+query_condition)

        order_ids = cursor.fetchall()
        all_time_slots = Order.getTimeSlot()

        for order_data in order_ids:
            order = Order(int(order_data[0]))
            order_info = order.getOrderInfo()
            user = User(order_info['user_id'])
            order_info['user'] = user.getObj()
            order_info['user']['wishlist'] = User.getWishlist(order_info['user_id'])
            order_info['address'] = user.getAddressInfo(order_info['address_id']) 
            order_info['delivery_slot'] = [ts for ts in all_time_slots if ts['slot_id'] == order_info['delivery_slot']][0]
            order_info['pickup_slot'] = [ts for ts in all_time_slots if ts['slot_id'] == order_info['pickup_slot']][0]
            order_info['comment'] = order_data[1]
            order_info['edited'] = order_data[2]
            order_info['delivered_by'] = order_data[3]
            order_info['delivery_amount'] = order_data[4]
            order_info['picked_by'] = order_data[5]
            order_info['pickup_amount'] = order_data[6]

            next_order_status = int(order_info['order_status'])+1
            order_info['change_status'] = {
                    'status_id': next_order_status, 
                    'status': Order.getOrderStatusDetails(next_order_status)['Status']
                    }
            order_info['order_status'] = Order.getOrderStatusDetails(order_info['order_status'])['Status']
            
            for i,inventory_id in enumerate(order_info['inventory_ids']):
                # check if item is in inventory
                order_copy = dict(order_info)
                cursor.execute("""SELECT isbn_13 FROM inventory WHERE inventory_id = %s""",(inventory_id,))
                isbn = cursor.fetchone()
                if isbn:
                    order_copy['isbn_13'] = isbn[0]
                order_copy['item'] = order_info['items'][i]
                order_copy['inventory_id'] = inventory_id
                del(order_copy['items'])
                del(order_copy['inventory_ids'])
                order_list.append(order_copy)

        return order_list

    @staticmethod
    def getPickups():
        orders_list = Admin.getCurrentOrders(pickups=True)
        for i,order in enumerate(orders_list):
            orders_list[i]['order_type'] = 'borrow'
            orders_list[i]['scheduled_date'] = order['order_return']
            orders_list[i]['scheduled_slot'] = order['pickup_slot']
             # NOTE removing charge of first order
            if len(order['all_charges']) == 1 and order['charge'] == order['all_charges'][0]['charge']:
                order['charge'] = 0
        
        rental_list = Admin.getCurrentRentals(returns=True)
        for i,rental in enumerate(rental_list):
            rental_list[i]['order_type'] = 'lend'
            rental_list[i]['scheduled_date'] = rental['delivery_date']
            rental_list[i]['scheduled_slot'] = rental['delivery_slot']
        
        history_orders = []
        date = datetime.now().date()
        for order in orders_list:
            order_return = datetime.strptime(order['order_return'], "%Y-%m-%d %H:%M:%S").date()
            if order_return < date:
                history_orders.append(order)

        for order in history_orders:
            orders_list.remove(order)

        return orders_list+rental_list+history_orders

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
    @async
    def updateOrderComment(data):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""UPDATE orders_admin_notes SET 
                comment = %s, 
                edited = %s,
                delivered_by = %s,
                delivery_amount = %s,
                picked_by = %s,
                pickup_amount = %s
                WHERE order_id = %s AND order_type = %s""",
        (data['comment'], data['edited'], data['delivered_by'], data['delivery_amount'], 
        data['picked_by'], data['pickup_amount'], data['order_id'], data['order_type']))
        conn.commit()
        affected = cursor.rowcount
        if not affected:
            cursor.execute("""INSERT INTO orders_admin_notes (order_id, order_type, comment, edited)
                VALUES (%s, %s, %s, %s)""", (data['order_id'], data['order_type'], data['comment'], data['edited']))
            conn.commit()
        return True

    @staticmethod
    def insertItem(data):        
        conn = mysql.connect()
        cursor = conn.cursor()
    
        if 'author' in data['goodreads'] and data['goodreads']['author']:
            author = data['goodreads']['author']
        elif 'author' in data['amazon'] and data['amazon']['author']:
            author = data['amazon']['author']
        else:
            author = ''

        cursor.execute("""SELECT item_id FROM items WHERE item_name LIKE %s AND author LIKE %s""", (data['amazon']['title'], author))
        match = cursor.fetchone()
        if match:
            return {'_id': int(match[0])}

        price = data['amazon']['list_price'] if data['amazon']['list_price'] else data['amazon']['offer_price']
        price = re.sub('\..*$', '', price)
        price = price.replace(',','')

        summary = ''
        if 'gr_summary' in data['goodreads'] and data['goodreads']['gr_summary']:
            summary = data['goodreads']['gr_summary']
        elif 'amzn_summary' in data['amazon']:
            for key in data['amazon']['amzn_summary']:
                if data['amazon']['amzn_summary'][key]:
                    summary = data['amazon']['amzn_summary'][key]
                    break
        slug_url = slugify(data['amazon']['title'])[:100]

        cursor.execute("""INSERT INTO items (item_name, price, author, ratings,
        num_ratings, num_reviews, language, asin, goodreads_id, summary, slug_url) VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        (data['amazon']['title'],
        price,
        author,
        data['goodreads']['avg_rating'].replace(' rating',''),
        data['goodreads']['num_ratings'].replace(' rating',''),
        data['goodreads']['num_review'],
        data['goodreads']['language'],
        data['amazon']['amazon_id'],
        data['goodreads']['gr_id'],
        summary,
        slug_url
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
                    else:
                        cursor.execute("""INSERT INTO categories (category_name) VALUES (%s)""",
                                (genre,))
                        conn.commit()
                        global_categories[genre] = cursor.lastrowid
                        cursor.execute("""INSERT INTO items_categories (item_id, category_id)
                        VALUES (%s, %s)""",(item_id, global_categories[genre]))


                conn.commit()

        s3conn = S3Connection('AKIAIN4EU63OJMW63H6A', 'k97pZ8rmwkqLdeW+L4QOIKrCDIg3YR/uY/BifLU3')
        bucket = s3conn.get_bucket('ostrich-catalog')
        basepath = webapp.config['S3_IMAGE_BUCKET']

        if 'img_small' in data['amazon'] and data['amazon']['img_small']:
            url = data['amazon']['img_small']
        elif 'img_large' in data['amazon'] and data['amazon']['img_large']:
            url = data['amazon']['img_large']

        if url:
            parsed = urlparse.urlparse(url)
            ext =  os.path.splitext(parsed.path)[1]
            path = basepath + str(item_id) + ext
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
        #if not db.items.find({'_id': final_data['_id']}).count():
        #    db.items.insert_one(final_data)
        db.items.update_one({'_id': int(item_id)}, {'$set': final_data}, upsert=True)
        final_data['item id'] = item_id
        return final_data

    @staticmethod
    def savePanelData(data):
        client =  MongoClient(webapp.config['MONGO_DB'])
        db = client.ostrich
        panel_data = {
            'title': data['title'],
            'items': data['items'].split(',') 
        }
        db.content.update_one(
                {'_id': ObjectId(data['_id'])},
                {'$set': panel_data}
                )
        
        Notifications().startDataUpdate() 
        return True

    @staticmethod
    def getSearchFailedQueries():
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT * FROM search_fails WHERE flow != 'admin' AND item_id IS NULL 
                ORDER BY timestamp DESC LIMIT 50""")
        numrows = cursor.rowcount
        data = []
        for i in range(numrows):
            data.append(Utils.fetchOneAssoc(cursor))
        return data
    
    @staticmethod
    def submitSearchFailItem(args):
        conn = mysql.connect()
        cursor = conn.cursor()

        if args['item_id']:
            update_field = "item_id = %s"
            update_field_values = (args['item_id'], args['query_id'])
        elif args['query']:
            update_field = "refined_query = %s, type = %s"
            update_field_values = (args['query'], args['query_type'], args['query_id'])

        cursor.execute("""UPDATE search_fails SET """+update_field+""" WHERE id = %s""",
                update_field_values)
        conn.commit()
        return True

    @staticmethod
    def sendSearchFailNotification(data):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM search_fails WHERE id = %s""",(data['query_id'],))
        search_data = cursor.fetchone()
        if not search_data[6] and not search_data[7]:
            return
        if search_data[1] <= 0 and not search_data[8]:
            return
      
        if search_data[1] <= 0 and search_data[8]:
            user_gcm_id = search_data[8]
        else:
            user = User(int(search_data[1]))
            user_gcm_id = user.gcm_id

        notification_data = {
                    "title": "Book Now Available",
                    "search_intention": search_data[5],
                    "bottom_text": "Ostrich Books"
                }
        if search_data[6]:
            item = Item(int(search_data[6]))
            item_name_ellipse = (item.item_name[:27] + '...') if len(item.item_name) > 27 else item.item_name

            notification_data['notification_id'] = 5
            notification_data['entity_id'] = item.item_id
            notification_data['item_name'] = item.item_name
            notification_data['message'] = "\""+item_name_ellipse+"\" is now available"
            notification_data['expanded_text'] = "\""+item.item_name+"\" is now available."

        elif search_data[7]:
            query_ellipse = (search_data[7][:27] + '...') if len(search_data[7]) > 27 else search_data[7]
            if search_data[4] == "author":
                notification_data['message'] = "Books by \""+query_ellipse+"\" are now available"
                notification_data['expanded_text'] = "Books by \""+search_data[7]+"\" are now available"
            elif search_data[4] == "genre":
                notification_data['message'] = "\""+query_ellipse+"\" books are now available"
                notification_data['expanded_text'] = "\""+search_data[7]+"\" books are now available"
            else:
                notification_data['message'] = "\""+query_ellipse+"\" is now available"
                notification_data['expanded_text'] = "\""+search_data[7]+"\" is now available"

            
            notification_data['notification_id'] = 6
            notification_data['query'] = search_data[7]
            notification_data['query_name'] = search_data[7]
            notification_data['query_type'] = search_data[4]

        status = Notifications(user_gcm_id).sendNotification(notification_data) 
        if status and 'success' in status:
            cursor.execute("""UPDATE search_fails SET gcm_token = %s WHERE id = %s""", (json.dumps(status['success']), data['query_id']))
            conn.commit()
        return True

    @staticmethod
    def addItemToInventory(item_id):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO inventory (item_id, fetched) VALUES (%s,1)""",(item_id,))
        conn.commit()
        inventory_id = cursor.lastrowid
        item = Item(item_id).getObj()
        
        Indexer().indexItems(query_condition=' AND i.item_id='+str(item_id))
        return {'item': item, 'inventory_id': inventory_id}

    @staticmethod
    def updateAreas(data):
        conn = mysql.connect()
        cursor = conn.cursor()
        hours = Utils.getParam(data, 'hours', 'int', None)
        day = Utils.getParam(data, 'day', 'int', None)
        slot = Utils.getParam(data, 'slot', 'int', None)
        alias_id = Utils.getParam(data, 'alias_id', 'int', None)
        active = Utils.getParam(data, 'active', 'int', 1)

        if 'area_id' in data:
            cursor.execute("""UPDATE areas SET name = %s, hours = %s, day = %s, slot = %s, alias_id = %s, active = %s WHERE area_id = %s""", 
                    (data['name'], hours, day, slot, alias_id, active, int(data['area_id'])))
            conn.commit()
        else:
            cursor.execute("""INSERT INTO areas (name, hours, day, slot, alias_id) VALUES (%s,%s,%s,%s,%s)""", 
                    (data['name'], hours, day, slot, alias_id))
            conn.commit()

        cursor.execute("""SELECT address_id, locality, gcm_id FROM user_addresses ua 
                INNER JOIN users u ON u.user_id = ua.user_id
                WHERE LOWER(locality) = %s""",
                (data['name'].lower(),)) 
        addresses = cursor.fetchall()

        for address in addresses:
            validation = User.validateLocality(address[1])
            validation['validated_locality'] = validation['validated_locality'] if validation['is_valid'] else data['name']

            cursor.execute("""UPDATE user_addresses SET is_valid = %s, delivery_message = %s, locality = %s WHERE address_id = %s""",
                    (validation['is_valid'], validation['delivery_message'], validation['validated_locality'], address[0]))
            conn.commit()
            Notifications(address[2]).startDataUpdate()
        return True

    @staticmethod
    def updateBookShotsData(rows):
        ####### Rows #########
        # Book id (optional)
        # Book Title
        # Genre 1
        # Genre 2
        # Genre 3
        # meta_description
        # for_whom
        # read_by
        # num_readers
        # trivia
        # amzn_link
        # amzn_delivery
        # amzn_price
        # fk_link
        # fk_delivery
        # fk_price
        ###########
        conn = mysql.connect()
        cursor = conn.cursor()

        for row in rows:
            try:
                if not row[0] or (row[0] and not row[0].isdigit()):
                    cursor.execute("SELECT item_id FROM items WHERE item_name = %s", (row[1],))
                    row[0] = cursor.fetchone()[0]
                del(row[1])
                del(row[7])
                cursor.execute("""INSERT INTO bs_items (item_id, genre1, genre2, genre3,
                    meta_description, for_whom, read_by, trivia, amzn_link, 
                    amzn_delivery, amzn_price, fk_link, fk_delivery, fk_price) VALUES
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE
                    genre1 = %s,
                    genre2 = %s,
                    genre3 = %s,
                    meta_description = %s,
                    for_whom = %s,
                    read_by = %s,
                    trivia = %s,
                    amzn_link = %s,
                    amzn_delivery = %s,
                    amzn_price = %s,
                    fk_link = %s,
                    fk_delivery = %s,
                    fk_price = %s""", tuple(row + row[1:]))
                conn.commit() 
            except e:
                print str(e)

        return True
        #cursor.execute("SELECT * FROM bs_items")
        #rows = [list(row) for row in cursor.fetchall()]
        #return rows 
