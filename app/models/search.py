from app import webapp
from app import mysql
from app.models import Item

class Search():

    @staticmethod
    def searchQuery(q, page=1):

        limit = page * 20
        offset = (page-1) *20

        connect = mysql.connect()
        search_cursor = connect.cursor()
        search_cursor.execute("SELECT item_id FROM items WHERE item_name LIKE \
                '%%%s%%' OR author LIKE '%%%s%%' LIMIT %d OFFSET %d" %(q, q, limit, offset))
        results = search_cursor.fetchall()
        search_cursor.close()

        refined_results = []
        for item_id in results:
            item = Item(item_id[0])
            refined_results.append(item.getObj())

        return refined_results

        search_cursor = self.connect.cursor()
        search_cursor.execute("SELECT i.item_id FROM items i \
                        LEFT JOIN items_categories ic ON i.item_id = ic.item_id \
                        LEFT JOIN categories c ON c.category_id = ic.category_id \
                        WHERE c.category_name LIKE '%%%s%%' LIMIT %d" %(q, 200-len(refined_results))) 
        results = search_cursor.fetchall()
        search_cursor.close()

        for item_id in results:
            if len(refined_results) <= 20:
                item = Item(item_id[0])
                refined_results.append(item_id.getObj())

        return refined_results        


    @staticmethod
    def searchQueryByType(q, qtype, page=1):

        limit = page * 20
        offset = (page-1) *20

        if qtype == "title":
            query = "SELECT item_id FROM items WHERE item_name LIKE \
                '%%%s%%' LIMIT %d OFFSET %d"
        elif qtype == "genre":
            query = "SELECT i.item_id FROM items i \
                LEFT JOIN items_categories ic ON i.item_id = ic.item_id \
                LEFT JOIN categories c ON c.category_id = ic.category_id \
                WHERE c.category_name LIKE '%%%s%%' LIMIT %d OFFSET %d"

        connect = mysql.connect()
        search_cursor = connect.cursor()
        search_cursor.execute(query % (q, limit, offset))
        results = search_cursor.fetchall()
        search_cursor.close()

        refined_results = []
        for item_id in results:
            item = Item(item_id[0])
            refined_results.append(item.getObj())


        return refined_results


