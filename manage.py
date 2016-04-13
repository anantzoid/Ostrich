from flask.ext.script import Manager
from app import webapp

manager = Manager(webapp)

@manager.command
def hello():
    from app.scripts.crawl_items_summary import crawl_items
    crawl_items()

@manager.command
def session():
    from app.models import Notifications
    Notifications().startDataUpdate()

@manager.command
def indexer():
    from app.scripts import Indexer
    custom_keys = {
            'custom_price': 60
            }
    Indexer().indexItems(query_condition=' AND (i.price <= 200)',limit='10',custom_keys=custom_keys)

@manager.command
def indexcol():
    from app.scripts import Indexer
    Indexer().indexCollections()

if __name__ == "__main__":
    manager.run()
