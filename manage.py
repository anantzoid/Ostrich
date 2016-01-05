from flask.ext.script import Manager
from app import webapp

manager = Manager(webapp)

@manager.command
def hello():
    from app.scripts.pickup_schedule import pickupSchedule
    pickupSchedule()

@manager.command
def indexer():
    from app.scripts import Indexer
    Indexer().getAllDataFromDB(query_condition=' AND i.item_id IN (SELECT item_id FROM mongo_mapping WHERE item_id > 3775 ORDER BY item_id ASC)')

if __name__ == "__main__":
    manager.run()
