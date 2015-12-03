from flask_mail import Message
from app import mail

class Mailer():
    @staticmethod
    def excessOrder(user_id, item_id):
        recipient = "anant718@gmail.com"
        sender = "anant718@hotmail.com"

        email  = Message("Excess Order Request",
                        sender=sender)
        email.recipients = [sender]
        email.body = "%s Tried to order Item %s" %(user_id, item_id)
        try:
            mail.send(email)
        except Exception,e:
            print str(e)
