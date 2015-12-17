from flask.ext.script import Manager
from app import webapp

manager = Manager(webapp)

@manager.command
def hello():
    print "yayay"

@manager.command
def indexer():
    from app.scripts import Indexer
    Indexer().getAllDataFromDB()

if __name__ == "__main__":
    manager.run()
