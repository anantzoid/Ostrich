import requests
import json
import re
from bs4 import BeautifulSoup as bs
from app.models import *
from app import webapp, mysql
from pymongo import MongoClient
import urllib3
from datetime import datetime
urllib3.disable_warnings()

amazon_search_url = 'http://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Dstripbooks&field-keywords='
client = MongoClient(webapp.config['MONGO_DB'])
db = client.ostrich

def getRelatedItems(item_id):
    related_items_data = [_ for _ in db.related_item_ids.find({'_id':item_id})]
    if related_items_data:
        return

    item = Item(item_id)
    url = amazon_search_url+item.item_name+' '+item.author
    soup = prepareSoup(url)

    link = soup.find('a', {'class':'s-access-detail-page'}) 
    if link and 'href' in link.attrs: 
        item_url = link.attrs['href'] 
        print item_url
        soup = checkForPaperback(item_url)
        
        amazon_id = 0
        book_id = soup.find('input', {'id':'ASIN'})
        if book_id:
            amazon_id = book_id.attrs['value']
        print amazon_id
        related_items_ids = []
        try:
            carousel = soup.find('div',{'class':'a-carousel-container'})
            if carousel:
                carousel_data = carousel.attrs["data-a-carousel-options"]
                carousel_data = json.loads(carousel_data)
                item_id_list = carousel_data['ajax']['id_list']
                storeRelatedItemIds(amazon_id, item_id_list)
                related_items_ids = fetchRelatedItemsData([_ for _ in item_id_list[:4]])
        except:
            item_links = []
            cards = soup.findAll('li', {'class': 'a-carousel-card'})
            for card in cards:
                link = card.find('a', {'class':'a-link-normal'})
                if link:
                    item_links.append(findAmazonIdFromUrl(link.attrs['href']))
            related_items_ids = fetchRelatedItemsData(item_links)

        print related_items_ids
        db.related_item_ids.insert_one({"_id":item_id,"item_ids":related_items_ids})
        

#### Helper Functions ####
def prepareSoup(url):
    resp = requests.get(url)
    soup = bs(resp.text, "html.parser") 
    return soup

def checkForPaperback(item_url):
    soup = prepareSoup(item_url)
    book_type = soup.findAll('li', {'class': 'swatchElement'})
    for types in ["Paperback", "Hardcover"]:
        for b_type in book_type:
            if types in b_type.text:
                if 'unselected' in b_type.attrs['class']:
                    item_url = b_type.find('a')
                    if item_url:
                        soup = prepareSoup('http://www.amazon.in/'+item_url.attrs['href'])
                return soup
    return soup

def storeRelatedItemIds(item_id, item_id_list):
    if not db.related_items_amazon_ids.find({"_id":item_id}).count():
        db.related_items_amazon_ids.insert_one({"_id":item_id,"item_ids":item_id_list})

def findAmazonIdFromUrl(item_link):
    groups = re.search('\/(B\d{3}\w{6}|\d{9}(?:X|\d))\/?', item_link)
    if groups:
        return groups.group(1)
    return item_link

def fetchRelatedItemsData(item_links):
    # Get items ids of related amazon ids
    # Insert new item if it doesn't exist already

    related_item_ids = []
    cursor = mysql.connect().cursor()
    for link in item_links:
        print 'amazon_id:',link
        item_data = getAggregatedBookDetails('http://www.amazon.in/dp/'+link) 
        item_data['timestamp'] = str(datetime.now()) 

        cursor.execute("""SELECT item_id FROM mongo_mapping WHERE amazon_id = %s""", (link,))
        item_id = cursor.fetchone()
        if item_id:
            item_id = int(item_id[0])
            related_item_ids.append(item_id)
            dumpItemData(item_data, item_id)
            continue

        try:
            isbns = tuple(re.sub('[^0-9]','', _) for _ in item_data['goodreads']['isbns'] + [item_data['goodreads']['isbn_13']] if len(_) >= 10)
            if isbns:
                format_char = ",".join(["%s"] * len(isbns))
                cursor.execute("""SELECT DISTINCT item_id FROM item_isbn WHERE isbn_13 IN ("""+format_char+""")""", isbns)
                item_id = cursor.fetchone()
                if item_id:
                    item_id = int(item_id[0])
                    related_item_ids.append(item_id)
                    dumpItemData(item_data, item_id)
                    continue
        except Exception, e:
            print isbns, str(e)

        cursor.execute("""SELECT DISTINCT item_id FROM items WHERE item_name = %s""",(re.sub('\(.*\)','', item_data['amazon']['title']),))
        item_id = cursor.fetchone()
        if item_id:
            item_id = int(item_id[0])
            related_item_ids.append(item_id)
            dumpItemData(item_data, item_id)
            continue
          
        final_data = Admin.insertItem(item_data)
        related_item_ids.append(final_data['_id'])

    return related_item_ids

def dumpItemData(item_data, item_id):
    print 'item_id:', item_id
    print 'item_name:',item_data['amazon']['title']
    final_data = item_data['goodreads']
    final_data.update(item_data['amazon'])
    final_data['_id'] = int(item_id)

    db.items.delete({'_id': final_data['_id']})
    db.items.insert_one(final_data)
    #db.items.update_one({'_id': final_data['_id']}, {'$set': final_data}, upsert=True)
