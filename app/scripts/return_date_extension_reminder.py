from app import mysql 
from app.models import Utils
from app.models import User
from app.models import Order
from app.models import Notifications

def returnDateExtensionReminder(): 
    current_timestamp = Utils.getCurrentTimestamp()
    return_date = Utils.getDefaultReturnTimestamp(current_timestamp, 3)

    cursor = mysql.connect().cursor()
    cursor.execute("""SELECT order_id, user_id
        FROM orders 
        WHERE DATE(order_return) = DATE('%s')
        """ % (return_date))
    query_data = Utils.fetchOneAssoc(cursor)

    user = User(query_data['user_id'])
    order = Order(query_data['order_id'])
    
    notification_data = {
            "type": "order_extension",
            "id": order.order_id,
            }
    temp_gcm_id = 'dTKtMjUPSho:APA91bGy3oVY680azB-jNmdAlDyRBCswnRaNg17naVkCXfTe88mSfJETB5BZTXO1dDaQJiCd7lUoDccJt3asT04nfWDj8gaghquqwjgIFUEuCZ2w4RojeTA4fQAsWNhVThSWWlASJ7NE'
    Notifications(temp_gcm_id).sendNotification(notification_data)

    
        

