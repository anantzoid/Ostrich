from app import mysql
from datetime import datetime
from app import webapp
from app.models import *
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime

class User(Prototype):
    def __init__(self, user_id, login_type='user_id'):
        self.getData(user_id, login_type)
        self.available_areas = {"indiranagar":6,
                                "indira nagar":6,
                                "koramangala":6,
                                "domlur":6,
                                "kodihalli":6,
                                "binnamangala":6,
                                "doopanahalli":6,
                                "adugodi":6,
                                "embassy golflinks":6,
                                "embassy golf links":6,
                                "challaghatta":6}

    def getData(self, user_id, login_type):

        get_data_query = "SELECT u.user_id, u.username, u.name, u.email, u.phone, u.google_id, \
                u.gcm_id, u.date_created, ui.invite_code, uw.wallet_id, uw.amount as wallet_balance FROM users u \
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
   

    def getObj(self):
        user_obj = vars(self)
        user_obj = user_obj['data']
        if not user_obj:
            user_obj = None
        return user_obj

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
    
        #TODO handle facebook_id
        google_id = user_data['google_id'] if 'google_id' in user_data else ''
        gcm_id = user_data['gcm_id'] if 'gcm_id' in user_data else ''

        
        if email:
            check_email_cursor = conn.cursor()
            check_email_cursor.execute("SELECT user_id FROM users WHERE email = '%s'" %(email))
            user_exists_id = check_email_cursor.fetchone()
            check_email_cursor.close()

            if user_exists_id and len(user_exists_id):
                user_exists = User(int(user_exists_id[0]), 'user_id')
                return {'message': 'Email exists', 'user': user_exists.getObj()} 

        create_user_cursor = conn.cursor()
        create_user_cursor.execute("INSERT INTO users (username, password, name, \
                email, phone, google_id, gcm_id) VALUES ('%s', '%s', '%s','%s', \
                '%s', '%s', '%s')" % (username, password, name, email, phone, google_id, gcm_id))
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

        # Welcome Mail
        Mailer.welcomeMailer(user)
       
        notification_data = {
                "notification_id": 100,
                "title": "Your wallet has been recharged!",
                "message": "Read first 3 books at no cost",
                "expanded_text": "You've earned 100 credits as an early sign up bonus. You can use these credits to order books for free!" 
                }

        Notifications(user.gcm_id).sendNotification(notification_data)

        return {'user': user.getObj()}


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

            conn = mysql.connect()
            insert_add_cursor = conn.cursor()

            if mode == 'insert':
                insert_add_cursor.execute("""INSERT INTO user_addresses 
                (user_id, address, description, locality, landmark, latitude, longitude) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (self.user_id, address, description, locality, landmark, lat, lng))
            elif mode == 'edit' and address_id:
                insert_add_cursor.execute("""UPDATE user_addresses SET address = %s,
                description = %s, landmark = %s, latitude = %s, longitude = %s 
                WHERE address_id = %s""", (address, description, landmark, lat, lng, address_id))
            conn.commit()
        
            address_ids.append(int(insert_add_cursor.lastrowid))
            insert_add_cursor.close()

        return address_ids


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
        return address_obj


    def validateUserAddress(self, address_obj):
        address_valid = False
        for address in self.address:
            if address['address_id'] == address_obj['address_id']:
                address_valid = True
                # Backsupport
                if 'address' in address_obj and address['address'] != address_obj['address']:
                    self.addAddress(address, mode='insert')
        return address_valid


    def getOrderSlots(self):
        from app.models import Order
        time_slots = {}

        for i,address in enumerate(self.address):
            interval = 0
            local_address = address['address'] if ('address' in address and address['address']) else address['locality']
            for area in self.available_areas.keys():
                if area in local_address.lower():
                    interval = self.available_areas[area]
                    break
            if interval:
                if interval not in time_slots:
                    time_slots[interval] = Order.getTimeSlotsForOrder(interval)
                self.address[i]['time_slot'] = time_slots[interval]

    @staticmethod
    def validateLocality(locality):
        for area in self.available_areas.keys():
            if area in locality.lower():
                response =  {"is_valid": 1, "delivery_message":"", "validated_locality":area}
                if area == "indira nagar":
                    response["validated_locality"] = "indiranagar"
                elif area == "kodihalli":
                    response["validated_locality"] = "indiranagar"
                elif area == "adugodi":
                    response["validated_locality"] = "koramangala"
                return response

        response =  {"is_valid": 0, "delivery_message":"Out of Delivery Area", "validated_locality":""}
        return response

    def getAllOrders(self):
        from app.models import Order 
        order_list = []
        orders_cursor = mysql.connect().cursor()
        orders_cursor.execute("""SELECT order_id
                FROM orders
                WHERE user_id = %d""" % (self.user_id))
        for order_id in orders_cursor.fetchall():
            order = Order(int(order_id[0]))
            order_info = order.getOrderInfo(formatted=True)
            #TODO item_id will be list in future
            order_info['items'] = [Item(int(order_info['item_id'])).getObj()]
            order_info['address'] = User.getAddressInfo(order_info['address_id']) 
            order_list.append(order_info)
        
        order_statuses = {"ordered":[], "reading":[], "previous":[]}
        for order in order_list:
            if order['order_status'] in [1, 2, 3]:
                order_statuses['ordered'].append(order)
            elif order['order_status'] == 4:
                order_statuses['reading'].append(order)
            elif order['order_status'] in [5, 6]:
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
            inv_info['pickup_time'] = Utils.formatTimeSlot(ts)

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
        timedelta = datetime.now() - user_created_datetime
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
