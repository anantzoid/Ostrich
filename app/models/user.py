from app import mysql
from datetime import datetime
from app import webapp
from app.models import *
from app.decorators import async
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
import json
import pytz

class User(Prototype):
    def __init__(self, user_id, login_type='user_id'):
        self.getData(user_id, login_type)

    def getData(self, user_id, login_type):

        get_data_query = "SELECT u.user_id, u.username, u.name, u.email, u.phone, u.google_id, \
                u.gcm_id, u.picture_url, u.date_created, ui.invite_code, uw.wallet_id, uw.amount as wallet_balance FROM users u \
                LEFT JOIN user_invite_codes ui ON ui.user_id = u.user_id \
                LEFT JOIN user_wallet uw ON uw.user_id = u.user_id \
                WHERE u.%s = %d" 
        if login_type != 'user_id':
            get_data_query = get_data_query.replace("%d", "'%s'")
        else:
            user_id = int(user_id)

        obj_cursor = mysql.connect().cursor()
        obj_cursor.execute(get_data_query % (login_type, user_id))
        self.data = Utils.fetchOneAssoc(obj_cursor)
        if not self.data: 
            self.data = {}
        else:
            self.data['address'] = []
            obj_cursor.execute("SELECT * FROM user_addresses WHERE \
                    user_id = %d" % (self.user_id))
            num_address = obj_cursor.rowcount
            for i in range(num_address):
                self.data['address'].append(Utils.fetchOneAssoc(obj_cursor))

            if not self.picture_url:
                self.picture_url = '/static/img/profile_default.jpg'
   

    @staticmethod
    def createUser(user_data):
       
        conn = mysql.connect()
        #TODO place order type validation
        username = user_data['username'] if 'username' in user_data else ''
        password = user_data['password'] if 'password' in user_data else ''
        if password:
            password = generate_password_hash(password)

        name = user_data['name'] if 'name' in user_data else ''
        phone = user_data['phone'] if 'phone' in user_data else ''
        email = user_data['email'] if 'email' in user_data else ''

        address = Utils.getParam(user_data, 'address')
    
        google_id = user_data['google_id'] if 'google_id' in user_data else ''
        gcm_id = user_data['gcm_id'] if 'gcm_id' in user_data else ''
        picture_url = user_data['picture_url'] if 'picture_url' in user_data else ''
        
        if email:
            check_email_cursor = conn.cursor()
            check_email_cursor.execute("SELECT user_id FROM users WHERE email = '%s'" %(email))
            user_exists_id = check_email_cursor.fetchone()
            check_email_cursor.close()

            if user_exists_id and len(user_exists_id):
                user_exists = User(int(user_exists_id[0]), 'user_id')
                user_exists.existed = "true"
                return user_exists

        create_user_cursor = conn.cursor()
        create_user_cursor.execute("""INSERT INTO users (username, password, name,
                email, phone, google_id, gcm_id, picture_url, last_app_version, 
                last_used_timestamp) 
                VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)""",
            (username, password, name, email, phone, google_id, gcm_id, picture_url, user_data['app_version']))
        conn.commit()

        user_id = int(create_user_cursor.lastrowid)
        create_user_cursor.close()
        user = User(user_id, 'user_id')

        if address: 
            user.addAddress(address)
        user.data['invite_code'] = user.setInviteCode()

        # Free credits on signup
        if not webapp.config['APP_INVITE']:
            Wallet.creditTransaction(user.wallet_id, user.user_id, 'signup', user.user_id)
            notification_data = {
                    "notification_id": 100,
                    "title": "Wallet Recharged",
                    "message": "Early sign-up bonus. Read the first 2 books at no cost.",
                    "expanded_text": "You've earned 100 credits as an early sign up bonus. Use these free credits to order a book now." 
                    }
            Notifications(user.gcm_id).sendNotification(notification_data)

        # Welcome Mail
        Mailer.welcomeMailer(user)
        user.removeFromUnregistered()
        return user


    def addAddress(self, address, mode='insert'):
        address = json.loads(address)
        if isinstance(address, dict):
            address = [address]

        address_ids = []
        for address_obj in address:
            address_id = Utils.getParam(address_obj, 'address_id')
            address = Utils.getParam(address_obj, 'address')
            lat = Utils.getParam(address_obj, 'latitude')
            lng = Utils.getParam(address_obj, 'longitude')
            
            #V2 information
            description = Utils.getParam(address_obj, 'description')
            locality = Utils.getParam(address_obj, 'locality')
            landmark = Utils.getParam(address_obj, 'landmark')
            is_valid = Utils.getParam(address_obj, 'is_valid')
            delivery_message = Utils.getParam(address_obj, 'delivery_message')
            
            conn = mysql.connect()
            insert_add_cursor = conn.cursor()

            if mode == 'insert':
                insert_add_cursor.execute("""INSERT INTO user_addresses 
                (user_id, address, description, locality, landmark, latitude, longitude,
                is_valid, delivery_message) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (self.user_id, address, description, locality, landmark, lat, lng, is_valid, delivery_message))
            elif mode == 'edit' and address_id:
                insert_add_cursor.execute("""UPDATE user_addresses SET address = %s,
                description = %s, landmark = %s, latitude = %s, longitude = %s,
                is_valid = %s, delivery_message = %s
                WHERE address_id = %s""", (address, description, landmark, lat, lng, address_id, is_valid, delivery_message))
            conn.commit()
        
            address_ids.append(int(insert_add_cursor.lastrowid))
            insert_add_cursor.close()

        return address_ids

    @async
    def removeFromUnregistered(self):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM users_unregistered WHERE gcm_id = %s""",
                (self.gcm_id,))
        conn.commit()
        return True

    def editDetails(self, user_data):
        username = user_data['username'] if 'username' in user_data else self.username
        name = user_data['name'] if 'name' in user_data else self.name
        phone = user_data['phone'] if 'phone' in user_data else self.phone
        email = user_data['email'] if 'email' in user_data else self.email
        gcm_id = user_data['gcm_id'] if 'gcm_id' in user_data else self.gcm_id 
        address = Utils.getParam(user_data, 'address')

        conn = mysql.connect()
        edit_user_cursor = conn.cursor()
        edit_user_cursor.execute("UPDATE users SET username = '%s', name = '%s', \
                phone = '%s', email = '%s', gcm_id = '%s' WHERE user_id = %d" % (username, name, \
                phone, email, gcm_id, self.user_id))
        conn.commit()
        edit_user_cursor.close()

        if address: 
            self.addAddress(address, mode='edit')

        return True

    @staticmethod
    def getAddressInfo(address_id):
        address_cusor = mysql.connect().cursor()
        address_cusor.execute("""SELECT * FROM user_addresses
                WHERE address_id = %d""" %(address_id))
        address_obj = Utils.fetchOneAssoc(address_cusor)
        return address_obj if address_obj else {}


    def validateUserAddress(self, address_obj):
        address_valid = False
        for address in self.address:
            if address['address_id'] == address_obj['address_id']:
                address_valid = True
                # Backsupport
                if 'address' in address_obj and address['address'] != address_obj['address']:
                    self.addAddress(json.dumps(address), mode='insert')
        return address_valid

    def getOrderSlots(self):
        from app.models import Order
        time_slots = {}
        address = self.address if self.address else []
        available_areas = Order.getAreasForOrder()
        for i,address in enumerate(address):
            selected_area = {}
            self.address[i]['time_slot'] = []

            for area in available_areas:
                if area in address['locality'].lower():
                    selected_area = available_areas[area]
                    break

            if selected_area:
                if selected_area['area_id'] not in time_slots:
                    if selected_area['hours']:
                        time_slots[selected_area['area_id']] = Order.getTimeSlotsForOrder(selected_area['hours'])
                    elif selected_area['day']:
                        dates = []
                        prev_date = 0
                        while len(dates) <= 4:
                            prev_date = prev_date + selected_area['day']
                            dates.append(Utils.fetchNextDayVerbose(prev_date))
                        
                        if selected_area['day'] == 1:
                            dates[0] = Utils.fetchNextDayVerbose('Today')

                        time_slots[selected_area['area_id']] = []
                        for date in dates:
                            ts = Order.getTimeSlot(selected_area['slot'])
                            ts['formatted'] = date['day']+' '+Utils.cleanTimeSlot(ts)
                            ts['delivery_date'] = date['date']
                            time_slots[selected_area['area_id']].append(ts)

                self.address[i]['time_slot'] = time_slots[selected_area['area_id']]

    @staticmethod
    def validateLocality(locality):
        from app.models import Order
        available_areas = Order.getAreasForOrder()
        response =  {"is_valid": 1, "delivery_message":"Delivery Available"}
        for area in available_areas:
            if area in locality.lower():
                response["validated_locality"] = area
                if available_areas[area]['alias_id']:
                    response["validated_locality"] = [_ for _ in available_areas if available_areas[_]['area_id'] == available_areas[area]['alias_id']][0]
                return response

        response =  {"is_valid": 0, "delivery_message":"Out of Delivery Area", "validated_locality":""}
        return response

    def getAllOrders(self):
        from app.models import Order 
        order_list = []
        orders_cursor = mysql.connect().cursor()
        orders_cursor.execute("""SELECT order_id
                FROM orders
                WHERE user_id = %d
                AND order_id NOT IN (SELECT DISTINCT parent_id FROM orders)""" 
                % (self.user_id))
        for order_id in orders_cursor.fetchall():
            order = Order(int(order_id[0]))
            order_info = order.getOrderInfo(formatted=True)
            order_info['address'] = User.getAddressInfo(order_info['address_id']) 
            order_info['extend_charges_slab'] = Item.getExtendRentalChargesSlab(order_info)
            order_list.append(order_info)
       
        for i in range(len(order_list)):
            if order_list[i]['parent_id']: 
                order_list[i] = Order.clubOrders(order_list[i]) 

        order_statuses = {"ordered":[], "reading":[], "previous":[]}
        for order in order_list:
            if order['order_status'] in [1, 2, 3]:
                order_statuses['ordered'].append(order)
            elif order['order_status'] == 4:
                order_statuses['reading'].append(order)
            elif order['order_status'] in [5, 6, 7]:
                #TODO NOTE Temp fix for app fuckup
                if order['order_status'] == 6:
                    order['order_status'] = 5
                order_statuses['previous'].append(order)
            
        return order_statuses

    def getAllRentals(self):
        from app.models import Order 
        inv_cursor = mysql.connect().cursor()
        inv_cursor.execute("""SELECT i.*, l.*
                FROM inventory i
                INNER JOIN lenders l ON l.inventory_id = i.inventory_id
                WHERE l. user_id = %d"""%(self.user_id))
        num_items = inv_cursor.rowcount
        inv_items = []
        for slot in range(num_items):
            inv_info = Utils.fetchOneAssoc(inv_cursor)
            inv_info['items'] = [Item(int(inv_info['item_id'])).getObj()]
            all_timeslots = Order.getTimeSlot()
            ts = [_ for _ in all_timeslots if _['slot_id'] == inv_info['pickup_slot']][0]
            inv_info['pickup_time'] = Utils.cleanTimeSlot(ts)
            inv_items.append(inv_info)

       
        rental_statses = {"rentals":[], "rental_history": []}
        current_timestamp = datetime.now() 
        for item in inv_items:
            date_removed = datetime.strptime(item['date_removed'], "%Y-%m-%d %H:%M:%S")
            diff = current_timestamp - date_removed
            if diff.days > 0:
                rental_statses["rental_history"].append(item)
            else:
                rental_statses["rentals"].append(item)
        return rental_statses


    @staticmethod
    def b2bUser(user_data):
        address = Utils.getParam(user_data, 'address', default=None)

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO b2b_users (email, phone, book_id, organization, address) VALUES
            (%s, %s, %s, %s, %s)""", (user_data['email'], user_data['phone'], user_data['book_id'], user_data['org'], address))
        conn.commit()
        Utils.notifyAdmin(-1, 'B2B User')
        return True

    @staticmethod
    def getWishlist(user_id):
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT item_id FROM wishlist WHERE user_id = %s AND active = 1""",
                (user_id,))
        item_ids = cursor.fetchall()

        wishlist = []
        if item_ids:
            item_ids = [int(_[0]) for _ in item_ids]
            wishlist = Search().getById(item_ids)
        return wishlist

    @staticmethod
    def addToWishlist(form_data):
        user_id = Utils.getParam(form_data, 'user_id', 'int')
        item_id = Utils.getParam(form_data, 'item_id', 'int')

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""SELECT COUNT(*) FROM wishlist WHERE user_id = %s AND item_id = %s""",
                (user_id, item_id))
        is_present = cursor.fetchone()
        if not is_present[0]:
            cursor.execute("""INSERT INTO wishlist (user_id, item_id) VALUES (%s,%s)""",
                    (user_id, item_id))
            conn.commit()
        else:
            cursor.execute("""UPDATE wishlist set active = 1, date_edited = CURRENT_TIMESTAMP
                    WHERE item_id = %s AND user_id = %s""", (item_id, user_id))
            conn.commit()
        return True

    @staticmethod
    def removeFromWishlist(form_data):
        user_id = Utils.getParam(form_data, 'user_id', 'int')
        item_id = Utils.getParam(form_data, 'item_id', 'int')

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""UPDATE wishlist set active = 0, date_edited = CURRENT_TIMESTAMP 
                WHERE item_id = %s AND user_id = %s""", (item_id, user_id))
        conn.commit()
        return True

    @async
    def logMetadata(self, app_version):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""UPDATE users SET last_app_version = %s, last_used_timestamp = 
                CURRENT_TIMESTAMP WHERE user_id = %s""", (app_version, self.user_id))
        conn.commit()

        client = MongoClient(webapp.config['MONGO_DB'])
        db = client.ostrich
        
        user_id = int(self.user_id)
        user_set = db.user_access_frequency.find({'_id':user_id}).count()
        if user_set:
            db.user_access_frequency.update({'_id': user_id}, 
                {'$addToSet': {'dates': datetime.now().strftime('%Y-%m-%d')}})
        else:
            db.user_access_frequency.insert({'_id': user_id,
                'dates': [datetime.now().strftime('%Y-%m-%d')]    
            })
        return True

    '''
        User Referral and Invite Functions
    '''
    def logReferral(self, uuid, source = 'phone'):
        conn = mysql.connect()

        log_ref_cursor = conn.cursor()
        log_ref_cursor.execute("INSERT INTO referrals (referrer_id, google_uuid, \
                source) VALUES (%d, '%s','%s')" %
                (self.user_id, uuid, source))
        conn.commit()
        referral_id = log_ref_cursor.lastrowid
        return referral_id


    def confirmReferral(self, uuid):
        if not self.isReferralValid():
            return False

        activation_date = Utils.getCurrentTimestamp()
        conn = mysql.connect()
        confirm_ref_cursor = conn.cursor()
        confirm_ref_cursor.execute("UPDATE referrals SET referent_id = %d, activated = %d, \
                activation_date = '%s' WHERE google_uuid = '%s'" % (self.user_id, 1, activation_date, uuid))
        conn.commit()
        if not confirm_ref_cursor.rowcount:
            return False
        else:
            referral_id = confirm_ref_cursor.lastrowid
            #NOTE instead of uuid, can extract referent id too
            Wallet.creditTransaction(self.wallet_id, self.user_id, 'referral', uuid)
        return True


    def isReferralValid(self):
        #TODO validity referent and referrer are not same, but the 5 minute check will handle that now
        #TODO replace time check with caching on signup
        user_created_datetime = datetime.strptime(self.date_created, '%Y-%m-%d %H:%M:%S')
        timedelta = datetime.now(pytz.timezone('Asia/Calcutta')) - user_created_datetime
        if timedelta.seconds > 300:
            return False
        else:
            if not self.isUserValidForReferral():
                return False
            else:
                return True


    def setInviteCode(self):
        invite_code = Utils.generateCode()

        conn = mysql.connect()
        set_code_cursor = conn.cursor()
        set_code_cursor.execute("INSERT INTO user_invite_codes (user_id, invite_code) \
                VALUES (%d, '%s')" %(self.user_id, invite_code))
        conn.commit()
        
        return invite_code
 

    def applyReferralCode(self, code):
        code_details = self.isCodeValid(code)
        if not code_details:
            return False
        else:
            [code_id, referrer_id] = code_details
            conn = mysql.connect()
            apply_code_cursor = conn.cursor()
            apply_code_cursor.execute("UPDATE user_invite_codes SET counter = counter +1 \
                    WHERE code_id = %d" % (code_id))
            conn.commit()
           
            log_referral_cursor = conn.cursor()
            log_referral_cursor.execute("INSERT INTO referrals (referrer_id, referent_id, \
                    activated, activation_date, source, source_id) VALUES (%d, %d, %d, '%s', '%s', \
                    %d)" % (referrer_id, self.user_id, 1, Utils.getCurrentTimestamp(), 'invite_code', code_id))
            conn.commit()
            referral_id = log_referral_cursor.lastrowid

            Wallet.creditTransaction(self.wallet_id, self.user_id, 'referral', referral_id)
            return True


    def isCodeValid(self, code):
        if not self.isUserValidForReferral():
            return False
        
        check_code_cursor = mysql.connect().cursor()
        check_code_cursor.execute("SELECT code_id, user_id FROM user_invite_codes WHERE \
                invite_code = '%s' AND user_id != %d" % (code, self.user_id))
        code_id = check_code_cursor.fetchone()
        if code_id:
            return [int(code_id[0]), int(code_id[1])] 
        else:
            return False


    def isUserValidForReferral(self):

        if not webapp.config['APP_INVITE']:
            return False

        check_user_cursor = mysql.connect().cursor()
        check_user_cursor.execute("SELECT referent_id FROM referrals WHERE referent_id = %d"
                % (self.user_id))
        if check_user_cursor.fetchone():
            return False
        else:
            return True

    @staticmethod
    def preregisterUser(email):
        conn = mysql.connect() 
        cursor = conn.cursor()
        cursor.execute("SELECT `id` FROM preregisters WHERE email = '%s'" % (email))
        result = cursor.fetchone()
        if not result:
            cursor.execute("INSERT INTO preregisters (email) VALUES ('%s')" % (email))
            conn.commit()

    @staticmethod
    def deleteUser(ids):
        from app.models import Order 
        conn = mysql.connect()
        cursor = conn.cursor()
        for user_id in ids:
            user_id = int(user_id)

            # TODO check if user is genuine and has lent an item
            cursor.execute("""SELECT inventory_id FROM lenders WHERE user_id = %d"""%(user_id))
            items = cursor.fetchall()
            inv_ids = []
            if items:
                for item in items:
                    inv_ids.append(str(item[0]))
                inv_ids = ",".join(inv_ids)
                cursor.execute("""DELETE FROM inventory WHERE inventory_id IN
                        ("""+inv_ids+""")""")
                conn.commit()

            cursor.execute("""DELETE FROM lenders WHERE user_id =%d"""%(user_id))
            conn.commit()

            cursor.execute("""DELETE FROM users WHERE user_id = %d"""%(user_id))
            conn.commit()

            cursor.execute("""DELETE FROM user_addresses WHERE user_id = %d"""
                    %(user_id))
            conn.commit()

            cursor.execute("""DELETE FROM user_invite_codes WHERE user_id = %d"""
                    %(user_id))
            conn.commit()

            cursor.execute("""DELETE FROM user_wallet WHERE user_id = %d"""
                    %(user_id))
            conn.commit()
       
            cursor.execute("""SELECT order_id FROM orders WHERE user_id = %d"""
                   %(user_id))
            orders = cursor.fetchall()
            for order_id in orders:
                Order.deleteOrder(int(order_id[0]))
            
        return
