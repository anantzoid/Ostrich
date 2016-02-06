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
        data['bottom_text'] = "Ostrich Books"
        if self.is_enabled and self.gcm_id:
            notification_status = self.gcm.json_request(registration_ids=self.gcm_id, data=data)
            return notification_status

