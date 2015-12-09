from flask_mail import Message
from app import mail
from app import webapp

class Mailer():
    @staticmethod
    def excessOrder(user_id, item_id):

        email  = Message("Excess Order Request", sender='anant718@gmail.com',
                recipients=['anant718@gmail.com'])
        email.body = "%d Tried to order Item %d" %(user_id, item_id)
        with webapp.app_context():
            mail.send(email)
