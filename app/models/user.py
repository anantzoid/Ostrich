from app import webapp
from app import mysql
from app.models import Helpers
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
