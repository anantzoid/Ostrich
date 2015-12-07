from gcm import GCM
from app import webapp

class Notifications():
    def __init__(self, gcm_id):
        self.gcm_id = gcm_id.split(",")
        self.gcm = GCM(webapp.config['GCM_API_KEY'])

    def sendNotification(self, data):
        notification_status = self.gcm.json_request(registration_ids=self.gcm_id, data=data)
        return notification_status

