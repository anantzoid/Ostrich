from app import webapp, mysql
from flask import request  
from app.models import *
import json

@webapp.route('/bookshots/books')
def getBooks():
    cursor = mysql.connect().cursor()
    cursor.execute("""SELECT * FROM bs_items""")
    books = []
    item_ids = []
    for i in range(cursor.rowcount):
        book_data = Utils.fetchOneAssoc(cursor)
        book_data['read_by'] = book_data['read_by'].split(',')
        book_data['for_whom'] = [_.strip().capitalize() for _ in book_data['for_whom'].split(',')]
        book_data['affiliate'] = {}
        item_ids.append(book_data['item_id'])
        books.append(book_data)
    item_objects = Search().getById(item_ids)

    for book in books:
        for i, item_object in enumerate(item_objects):
            if book['item_id'] == item_object['item_id']:
                item_objects[i].update(book)
                 
                genres = [_.capitalize() for _ in [book['genre1'], book['genre2'], book['genre3']] if _]
                item_objects[i]['categories'] = genres + item_objects[i]['categories'][:3-len(genres)]
                del(item_objects[i]['genre1'])
                del(item_objects[i]['genre2'])
                del(item_objects[i]['genre3'])
    return json.dumps(item_objects)
