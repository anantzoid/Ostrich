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
    Indexer().indexItems(query_condition=' AND (i.item_id = 410)',limit='10')

@manager.command
def indexcol():
    from app.scripts.extended_inv_match import ext_crawl
    ext_crawl()

if __name__ == "__main__":
    manager.run()
