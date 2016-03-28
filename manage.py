from flask.ext.script import Manager
from app import webapp

manager = Manager(webapp)

@manager.command
def hello():
    from app import mysql
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.executemany("insert into collections_metadata (collection_id, meta_key, meta_value) values (%s,%s,%s)",[(1,'1','1')])
    conn.commit()
    return
    from datetime import date, timedelta
    from app.scripts.get_unregistered_userdata import import_data
    yesterday = date.today() - timedelta(1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    import_data(yesterday, str(date.today()))
    exit(0)
    from app.scripts.upsell_email import upsellEmail
    upsellEmail(23)
    return
    from app.scripts.related_items import getRelatedItems
    getRelatedItems(4051)

@manager.command
def session():
    from app.models import Notifications
    Notifications().startDataUpdate()

@manager.command
def indexer():
    from app.scripts import Indexer
    custom_keys = {
            'out_of_stock': 1
            }
    Indexer().indexItems(query_condition=' AND (i.item_id = 217)',limit='',custom_keys=custom_keys)

@manager.command
def indexcol():
    from app.scripts import Indexer
    Indexer().indexCollections()

if __name__ == "__main__":
    manager.run()
