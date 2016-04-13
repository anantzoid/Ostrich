from app import mysql, webapp
from pymongo import MongoClient 
from app.models import *
import requests
from bs4 import BeautifulSoup as bs

amazon_search_url = 'http://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Dstripbooks&field-keywords='
def crawl_items():
    client =  MongoClient(webapp.config['MONGO_DB'])
    db = client.ostrich

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(""" SELECT * FROM (
            SELECT DISTINCT(item_id) FROM order_history  
            UNION
            SELECT DISTINCT(item_id) FROM collections_items) 
        item_id WHERE item_id NOT IN (SELECT item_id FROM items WHERE summary
        IS NOT NULL) limit 10""")
    item_ids = cursor.fetchall()

    for item_id in item_ids:
        item_id = int(item_id[0])
        print item_id
        record = [_ for _ in db.items.find({'_id':item_id, 'amzn_summary':{'$exists':True}})]
        if record:
            record = record[0]
        else:
            print "====Crawling===="
            item = Item(item_id)
            url = amazon_search_url+item.item_name+' '+item.author
            resp = requests.get(url)
            soup = bs(resp.text, "html.parser") 
            link = soup.find('a', {'class':'s-access-detail-page'}) 
            if link and 'href' in link.attrs: 
                amzn_url = link.attrs['href'] 
                data = getAggregatedBookDetails(amzn_url)

                record = data['goodreads']
                record.update(data['amazon'])
                db.items.update_one({'_id': item_id}, {'$set': record}, upsert=True)
    
        summary = ''
        gr_id = record['gr_id'] if 'gr_id' in record and record['gr_id'] else None
        amzn_id = record['amazon_id'] if 'amazon_id' in record and record['amazon_id'] else None
        if 'gr_summary' in record and record['gr_summary']:
            summary = record['gr_summary']
        elif 'amzn_summary' in record:
            for key in record['amzn_summary']:
                if record['amzn_summary'][key]:
                    summary = record['amzn_summary'][key]
                    break
        cursor.execute("""UPDATE items SET asin = %s, goodreads_id = %s,
        summary = %s WHERE item_id = %s""", (amzn_id, gr_id, summary, item_id))
        conn.commit()
 
                    
        

