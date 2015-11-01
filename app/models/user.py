from app import webapp
from app import mysql
from app.models import Item, Helpers
from werkzeug.security import generate_password_hash, check_password_hash
import json

class User():
    def __init__(self, user_id, login_type):
        self.getData(user_id, login_type)

    def __getattr__(self, field):
        if field in self.data:
            return self.data[field]
        else:
            return None

    
    def getData(self, user_id, login_type):

        get_data_query = "SELECT * FROM users WHERE %s = %d" 
        if login_type != 'user_id':
            get_data_query = get_data_query.replace("%d", "'%s'")
        else:
            user_id = int(user_id)

        obj_cursor = mysql.connect().cursor()
        obj_cursor.execute(get_data_query % (login_type, user_id))
        self.data = Helpers.fetchOneAssoc(obj_cursor)
        
        self.data['address'] = []
        obj_cursor.execute("SELECT * FROM user_addresses WHERE \
                user_id = %d" % (self.user_id))
        num_address = obj_cursor.rowcount
        for i in range(num_address):
            self.data['address'].append(Helpers.fetchOneAssoc(obj_cursor))

        if len(self.data['address']) == 1:
            self.data['address'] = self.data['address'][0]
   

    def getObj(self):
        user_obj = vars(self)
        user_obj = user_obj['data']
        # user_obj['user_id'] = self.user_id
        
        return user_obj


    @staticmethod
    def createUser(user_data):
        
        username = user_data['username'] if 'username' in user_data else ''
        password = user_data['password'] if 'password' in user_data else ''
        if password:
            password = generate_password_hash(password)

        name = user_data['name'] if 'name' in user_data else ''
        phone = user_data['phone'] if 'phone' in user_data else ''
        email = user_data['email'] if 'email' in user_data else ''

        address = Helpers.getParam(user_data, 'address')
    
        #TODO handle facebook_id
        google_id = user_data['google_id'] if 'google_id' in user_data else ''
        gcm_id = user_data['gcm_id'] if 'gcm_id' in user_data else ''

        
        if email:
            conn = mysql.connect()
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
            address = json.loads(address)
            address_id = user.addAddress(address)
         
        return {'user_id': user_id}
   

    def addAddress(self, address_obj):
        address = Helpers.getParam(address_obj, 'address')
        lat = Helpers.getParam(address_obj, 'latitude')
        lng = Helpers.getParam(address_obj, 'longitude')

        conn = mysql.connect()
        insert_add_cursor = conn.cursor()
        insert_add_cursor.execute("INSERT INTO user_addresses (user_id, address, \
                latitude, longitude) VALUES (%d, '%s', '%s', '%s')" % (self.user_id, \
                address, lat, lng))
        conn.commit()
        
        address_id = int(insert_add_cursor.lastrowid)
        insert_add_cursor.close()

        return address_id


    def editDetails(self, user_data):

        username = user_data['username'] if 'username' in user_data else self.username
        name = user_data['name'] if 'name' in user_data else self.name
        phone = user_data['phone'] if 'phone' in user_data else self.phone
        email = user_data['email'] if 'email' in user_data else self.email

        #TODO supporting only 1 address for now
        address = user_data['address'] if 'address' in user_data else self.address[self.address.keys()[0]]

        conn = mysql.connect()
        edit_user_cursor = conn.cursor()
        edit_user_cursor.execute("UPDATE users SET username = '%s', name = '%s', \
                phone = '%s', email = '%s' WHERE user_id = %d" % (username, name, \
                phone, email, self.user_id))
        conn.commit()
        edit_user_cursor.close()

        edit_address_cursor = conn.cursor()
        edit_address_cursor.execute("UPDATE user_addresses SET address = '%s' \
                 WHERE user_id = %d" % (address, self.user_id))
        conn.commit()
        edit_address_cursor.close()

        return True


    def getOrders(self):

        orders = {}
        orders['current'] = self.getCurrentOrder()
        orders['history'] = self.getOrderHistory()
        orders['rentals'] = self.getRentals()
        #TODO add rental history option

        return orders

    def getCurrentOrder(self):

        current_orders = []

        orders_cursor = mysql.connect().cursor()
        orders_cursor.execute("SELECT o.order_id, \
                o.order_placed, \
                o.order_status, \
                o.order_return, \
                o.pickup_slot, \
                o.delivery_slot, \
                a.address, \
                (select group_concat(oh.item_id SEPARATOR ',') FROM order_history oh \
                WHERE oh.order_id = o.order_id) AS item_ids \
                FROM orders o \
                INNER JOIN user_addresses a ON o.address_id = a.address_id \
                WHERE o.user_id = %d AND o.order_status <= 4" % (self.user_id))

        num_orders = orders_cursor.rowcount
        for i in range(num_orders):
            current_order = Helpers.fetchOneAssoc(orders_cursor)
            current_order['items'] = []
            if current_order['item_ids']:
                for item_id in current_order['item_ids'].split(","):
                    item = Item(int(item_id))
                    current_order['items'].append(item.getMinObj())

            del current_order['item_ids']
            current_orders.append(current_order)

        return current_orders
        

    def getOrderHistory(self):
        '''
            Separated from getCurrentOrder as cache will be implemented here
        '''

        order_history = []

        orders_cursor = mysql.connect().cursor()
        orders_cursor.execute("SELECT o.order_id, \
                o.order_placed, \
                o.order_return, \
                a.address, \
                (select group_concat(oh.item_id SEPARATOR ',') FROM order_history oh \
                WHERE oh.order_id = o.order_id) AS item_ids \
                FROM orders o \
                INNER JOIN user_addresses a ON o.address_id = a.address_id \
                WHERE o.user_id = %d AND o.order_status > 4" % (self.user_id))

        num_orders = orders_cursor.rowcount
        for i in range(num_orders):
            order = Helpers.fetchOneAssoc(orders_cursor)
            order['items'] = []
            if order['item_ids']:
                for item_id in order['item_ids'].split(","):
                    item = Item(int(item_id))
                    order['items'].append(item.getMinObj())

            del order['item_ids']
            order_history.append(order)

        return order_history


    def getRentals(self):

        rentals = []
        rental_cursor = mysql.connect().cursor()
        rental_cursor.execute("SELECT i.date_added, \
                i.item_id, \
                i.in_stock, \
                l.credit_id \
                FROM inventory i \
                INNER JOIN lender_credits l ON i.inventory_id = l.inventory_id \
                WHERE i.lender_id = %d" %(self.user_id))
        num_rentals = rental_cursor.rowcount
        for i in range(num_rentals):
            rental = Helpers.fetchOneAssoc(rental_cursor)
            if rental['item_id']:
                item = Item(int(rental['item_id']))
                rental['items'] = item.getMinObj()

            del rental['item_id']
            rentals.append(rental)
        print rentals
        return rentals


    @staticmethod
    def preregisterUser(email):
        conn = mysql.connect() 
        cursor = conn.cursor()
        cursor.execute("SELECT `id` FROM preregisters WHERE email = '%s'" % (email))
        result = cursor.fetchone()
        if not result:
            cursor.execute("INSERT INTO preregisters (email) VALUES ('%s')" % (email))
            conn.commit()


