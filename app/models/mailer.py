from flask import render_template
from flask_mail import Message
from app import mail
from app import webapp

class Mailer():
    @staticmethod
    def excessOrder(user_id, item_id):
        subject = "Excess Order Request"
        email  = Message(subject, 
                sender='contact@ostrichapp.in',
                recipients=['contact@ostrichapp.in'])
        email.body = "%d Tried to order Item %d" %(user_id, item_id)
        mail.send(email)
        return True

    @staticmethod
    def genericMailer(mail_obj):
        email = Message(mail_obj['subject'],
                    sender='contact@ostrichapp.in',
                    recipients=['contact@ostrichapp.in'])
        email.body = mail_obj['body']
        mail.send(email)
        return True
        

    @staticmethod
    def welcomeMailer(user):
        if user.name:
            name = user.name.split(" ")[0]
            if len(name) <=3:
                name = user.name
        else:
            name = 'there'
        name = name.capitalize()

        email = Message('Welcome to Ostrich!',
                    sender='contact@ostrichapp.in',
                    recipients=[user.email])
        email.html = render_template('welcome.html', name=name)
        mail.send(email)
        return True
