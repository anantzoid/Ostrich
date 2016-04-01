from flask.ext.script import Manager
from app import webapp

manager = Manager(webapp)

@manager.command
def hello():
    #from app.models import  AmazonCrawler
    #AmazonCrawler(url='http://www.amazon.in/Kite-Runner-Khaled-Hosseini/dp/1408850257/ref=tmm_pap_swatch_0?_encoding=UTF8&qid=&sr=').crawlPage()
    #return
    from app.scripts.related_items import getRelatedItems
    getRelatedItems(110)

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
