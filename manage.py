from flask.ext.script import Manager
from app import webapp

manager = Manager(webapp)

@manager.command
def hello():
    from app.models import User,Mailer
    Mailer.thankyou(User(1))

@manager.command
def indexer():
    from app.scripts import Indexer
    Indexer().indexItems(query_condition=' AND (i.item_id = 1 OR i.item_id=79)')

@manager.command
def searchfail():
    from app.models import Notifications, User, Item
    # user_id, item_id, flow
    data = [[76, 1, 'borrow', 1]]

    for row in data:
        user = User(row[0])
        Notifications(user.gcm_id).itemAvailability(row[1], row[2], row[3])

if __name__ == "__main__":
    manager.run()
