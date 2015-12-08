from flask.ext.script import Manager
from app import webapp
from app.scripts.test import test
from app.scripts.extension_reminder import extensionReminder

manager = Manager(webapp)

@manager.command
def hello():
    print "yayay"
    f = open("cronworks.txt","a")
    print >>f, test()

@manager.command
def reminder():
    extensionReminder()

if __name__ == "__main__":
    manager.run()
