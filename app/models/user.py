from app import webapp
from app import mysql
from werkzeug.security import generate_password_hash, check_password_hash
class User():
    def __init__(self, user_id):
        self.user_id = user_id

    @staticmethod
    def createUser(user_data):
        
        username = user_data['username'] if 'username' in user_data else ''
        password = user_data['password'] if 'password' in user_data else ''
        #TODO password validation
        if not password:
            return {'message': 'Password missing'}

        password = generate_password_hash(password)

        name = user_data['name'] if 'name' in user_data else ''
        phone = user_data['phone'] if 'phone' in user_data else ''
        email = user_data['email'] if 'email' in user_data else ''
        if not email:
            return {'message': 'Email missing'}

        google_id = user_data['google_id'] if 'google_id' in user_data else ''
        gcm_id = user_data['gcm_id'] if 'gcm_id' in user_data else ''
   

        conn = mysql.connect()


        check_email_cursor = conn.cursor()
        check_email_cursor.execute("SELECT user_id FROM users WHERE email = '%s'" %(email))
        record_count = check_email_cursor.fetchone()
        check_email_cursor.close()

        if record_count:
            return {'message': 'Email exists'} 

        create_user_cursor = conn.cursor()

        create_user_cursor.execute("INSERT INTO users (username, password, name, \
                email, phone) VALUES ('%s', '%s', '%s','%s', '%s')" % (username, password, \
                name, email, phone))
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


