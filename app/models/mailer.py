from flask import render_template
from flask_mail import Message
from threading import Thread
from app import mail
from app import webapp

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
    def genericMailer(mail_obj):
        email = Message(mail_obj['subject'],
                    recipients=['contact@ostrichapp.in'])
        email.body = mail_obj['body']
        mail.send(email)
        return True

    @staticmethod
    def getUserName(user):
        if user.name:
            name = user.name.split(" ")[0]
            if len(name) <=3:
                name = user.name
        else:
            name = 'there'
        name = name.capitalize()
        return name


    @staticmethod
    def welcomeMailer(user):
        name = Mailer.getUserName(user)
        email = Message('Welcome to Ostrich!',
                    recipients=[user.email])
        email.html = render_template('mailers/inlined/welcome.html', name=name)
        thr = Thread(target=Mailer.send_async_mail, args=[webapp, email])
        thr.start()
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
