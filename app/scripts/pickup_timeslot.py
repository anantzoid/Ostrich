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

    for num in range(num_items):
        query_data = Utils.fetchOneAssoc(cursor)
        user = User(query_data['user_id'])
        
        notification_data = {
            "notification_id": 3,
            "entity_id": query_data['order_id'],
            "message": "When should we come over to pickup tomorrow?"
            }
        Notifications(user.gcm_id).sendNotification(notification_data)

 
