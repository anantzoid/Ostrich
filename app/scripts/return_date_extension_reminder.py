from app import mysql 
from app.models import Utils
from app.models import User
from app.models import Notifications
from app.scripts.upsell_email import upsellEmail

def returnDateExtensionReminder(): 
    current_timestamp = Utils.getCurrentTimestamp()
    return_date = Utils.getDefaultReturnTimestamp(current_timestamp, 3)

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
                "notification_id": 1,
                "entity_id": query_data['order_id'],
                "title": "3 Days Left to Return the Book",
                "message": "Not finised yet? Extend the reading period.",
                "expanded_text": "You can extend the reading period by going to the order's page in \"My Orders\"."
                }
        Notifications(user.gcm_id).sendNotification(notification_data)
        upsellEmail(query_data['order_id'])


    
        

