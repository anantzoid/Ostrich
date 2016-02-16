from app import mysql
from app.models import Utils
from app.models import User, Order
from app.models import Notifications

def pickupTimeslot():
    current_timestamp = Utils.getCurrentTimestamp()
    return_date = Utils.getDefaultReturnTimestamp(current_timestamp, 1)

    cursor = mysql.connect().cursor()
    cursor.execute("""SELECT order_id, user_id, pickup_slot
            FROM orders
            WHERE DATE(order_return) = DATE('%s') AND order_id NOT IN
            (SELECT DISTINCT parent_id FROM orders)
            """ % (return_date))
    num_items = cursor.rowcount

    for num in range(num_items):
        query_data = Utils.fetchOneAssoc(cursor)
        user = User(query_data['user_id'])

        ts = Order.getTimeSlot(query_data['pickup_slot'])
        ts = Utils.cleanTimeSlot(ts)
        
        notification_data = {
            "notification_id": 1,
            "entity_id": query_data['order_id'],
            "title": "Return Date Tomorrow",
            "message": "Would you like to extend your reading period?",
            "expanded_text": "You can extend the reading period by going to the order's page in \"My Orders\". Otherwise, we'd contact you shortly to confirm your current pickup time: %s"%ts
            }

        Notifications(user.gcm_id).sendNotification(notification_data)

 
