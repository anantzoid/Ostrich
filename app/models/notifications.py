from gcm import GCM
from app import webapp
from app import mysql 
import json

class Notifications():
    def __init__(self, gcm_id):
        self.gcm_id = gcm_id.split(",") if gcm_id else 0
        self.gcm = GCM(webapp.config['GCM_API_KEY'])
        self.is_enabled = webapp.config['NOTIFICATIONS_ENABLED']

    def sendNotification(self, data):
        if self.is_enabled and self.gcm_id:
            notification_status = self.gcm.json_request(registration_ids=self.gcm_id, data=data)
            return notification_status

    def itemAvailability(self, item_id, flow, fail_id):
        from app.models import Item
        item = Item(item_id)
        data  = {
                "notification_id": 5,
                "entity_id": item.item_id,
                "title": "%s is now available" % (item.item_name),
                "message": "The book you were searching for is now available",
                "expanded_text": "The book you were searching for is now available",
                "item_name": item.item_name,
                "search_intention": flow
                }
        response = self.sendNotification(data)
        if 'success' in response:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("""UPDATE search_fails SET gcm_token = %s WHERE id = %s"""
                    ,(json.dumps(response['success']), fail_id))
            conn.commit()
