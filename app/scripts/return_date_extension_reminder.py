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

    f = open("/home/ubuntu/test_sup.log", "a")
    print >>f, query_data['user_id']+', '+query_data['order_id']

    user = User(query_data['user_id'])
    order = Order(query_data['order_id'])
    
    notification_data = {
            "type": "order_extension",
            "id": order.order_id,
            }
    Notifications(user.gcm_id).sendNotification(notification_data)

    
        

