from flask.ext.script import Manager
from app import webapp
from app.scripts.extension_reminder import extensionReminder

manager = Manager(webapp)

@manager.command
def hello():
    print "yayay"

@manager.command
def reminder():
    extensionReminder()

if __name__ == "__main__":
    manager.run()
