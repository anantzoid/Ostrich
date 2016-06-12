from flask import render_template
from flask_mail import Message
from threading import Thread
from app import mail
from app import webapp
from app.decorators import async
from premailer import Premailer, transform
from app.models import Utils

class Mailer():
    @staticmethod
    def send_async_mail(webapp, email):
        with webapp.app_context():
            mail.send(email)

    @staticmethod
    def excessOrder(user_id, item_id):
        subject = "Excess Order Request"
        email  = Message(subject, 
                recipients=['contact@ostrichapp.in'])
        email.body = "%d Tried to order Item %d" %(user_id, item_id)
        mail.send(email)
        return True

    @staticmethod
    def genericMailer(mail_obj, recipients=['contact@ostrichapp.in']):
        with webapp.app_context():
            email = Message(mail_obj['subject'],
                        recipients=recipients)
            email.body = mail_obj['body']
            mail.send(email)
        return True


    @staticmethod
    @async
    def welcomeMailer(user):
        name = Utils.getUserName(user)
        with webapp.app_context():
            email = Message('Welcome to Ostrich!',
                        recipients=[user.email])
            email.html = transform(render_template('mailers/welcome.html', name=name))
            mail.send(email)
        return True

    @staticmethod
    #TODO substitue @sync
    def thankyou(user):
        name = Mailer.getUserName(user)
        email = Message('Thank you for offering your book.',
                    recipients=[user.email])
        email.html = render_template('mailers/inlined/thank_you.html', name=name)
        thr = Thread(target=Mailer.send_async_mail, args=[webapp, email])
        thr.start()
        return True

    @staticmethod
    @async
    def sendUpsellEmail(data):
        name = Mailer.getUserName(data['user'])
        with webapp.app_context():
            consumer_mail = render_template('mailers/extend_order.html',
                            name = name,
                            book_name = data['book_name'],
                            order_id = data['order_id'],
                            items = data['items'], 
                            curated_items = data['curated_items'],
                            quote = data['quote'], 
                            quote_author = data['quote_author'])
            pre = Premailer(consumer_mail, remove_classes=False, strip_important=False)
            consumer_mail =  pre.transform()
            email = Message('Enjoying the book?',
                            recipients=[data['user'].email])
            email.html = consumer_mail
            mail.send(email)
        return True
