from app import mysql
from app.models import Utils
from app.models import User
from app.models import Notifications

def pickupTimeslot():
    current_timestamp = Utils.getCurrentTimestamp()
    return_date = Utils.getDefaultReturnTimestamp(current_timestamp, 1)

    cursor = mysql.connect().cursor()
    cursor.execute("""SELECT order_id, user_id
            FROM orders
            WHERE DATE(order_return) = DATE('%s')
            """ % (return_date))
    num_items = cursor.rowcount

    f = open("/home/ubuntu/extension_reminder1.log", "a")
    for num in range(num_items):
        query_data = Utils.fetchOneAssoc(cursor)
        print >>f, query_data.keys()[0]

        user = User(query_data['user_id'])
        print user.gcm_id
        
        notification_data = {
            "notification_id": 2,
            "entity_id": query_data['order_id'],
            "message": "When should we come over to pickup tomorrow?"
            }
        Notifications(user.gcm_id).sendNotification(notification_data)

 
