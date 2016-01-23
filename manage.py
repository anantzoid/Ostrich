from flask.ext.script import Manager
from app import webapp

manager = Manager(webapp)

@manager.command
def hello():
    from app.models import AmazonCrawler, GoodreadsCrawler
    data = AmazonCrawler(url='http://www.amazon.in/Our-Impossible-Love-Durjoy-Datta/dp/0143424610/ref=tmm_pap_swatch_0?_encoding=UTF8&qid=1453484827&sr=1-1').crawlPage()
    print data
    gr_data = GoodreadsCrawler(isbn=data['isbn13'],title='Our Impossible Love').startCrawl()
    if 'status' in gr_data and gr_data['status'] == 'error':
        gr_data = GoodreadsCrawler(isbn=data['isbn10']).startCrawl()
    print gr_data

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
