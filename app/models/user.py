from app import webapp
from app import mysql
from app.models import Helpers
from werkzeug.security import generate_password_hash, check_password_hash

class User():
    def __init__(self, user_id):
        self.user_id = user_id
        self.getData()

    def __getattr__(self, field):
        if field in self.data:
            return self.data[field]
        else:
            return None

    
    def getData(self):
        obj_cursor = mysql.connect().cursor()
        obj_cursor.execute("SELECT * FROM users WHERE user_id = %d" %(self.user_id))
        self.data = Helpers.fetchOneAssoc(obj_cursor)
        
        self.data['address'] = {}
        obj_cursor.execute("SELECT address_id, address FROM user_addresses WHERE \
                user_id = %d" % (self.user_id))
        for address in obj_cursor.fetchall():
            self.data['address'][int(address[0])] = address[1]
   
    def getObj(self):
        user_obj = vars(self)
        user_obj = user_obj['data']
        user_obj['user_id'] = self.user_id
        
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

        google_id = user_data['google_id'] if 'google_id' in user_data else ''
        gcm_id = user_data['gcm_id'] if 'gcm_id' in user_data else ''

        if email:
            conn = mysql.connect()
            check_email_cursor = conn.cursor()
            check_email_cursor.execute("SELECT user_id FROM users WHERE email = '%s'" %(email))
            record_count = check_email_cursor.fetchone()
            check_email_cursor.close()

            if record_count:
                return {'message': 'Email exists'} 

        create_user_cursor = conn.cursor()
        create_user_cursor.execute("INSERT INTO users (username, password, name, \
                email, phone, google_id, gcm_id) VALUES ('%s', '%s', '%s','%s', \
                '%s', '%s', '%s')" % (username, password, name, email, phone, google_id, gcm_id))
        conn.commit()

        user_id = int(create_user_cursor.lastrowid)
        user = User(user_id)
        create_user_cursor.close()
        
        return {'user_id': user_id}
   

    def addAddress(self, address):
        conn = mysql.connect()
        insert_add_cursor = conn.cursor()
        insert_add_cursor.execute("INSERT INTO user_addresses (user_id, address) \
                 VALUES (%d, '%s')" % (self.user_id, address))
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
