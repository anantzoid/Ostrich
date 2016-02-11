from flask.ext.script import Manager
from app import webapp

manager = Manager(webapp)

@manager.command
def hello():
    from app.scripts.upsell_email import upsellEmail
    upsellEmail(23)

@manager.command
def indexer():
    from app.scripts import Indexer
    Indexer().indexItems(query_condition=' AND (i.item_id = 1 OR i.item_id=79)')

if __name__ == "__main__":
    manager.run()
