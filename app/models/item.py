from app import webapp
from app import mysql


class Item():
    def __init__(self, item_id):
        self.item_id = item_id


    @staticmethod
    def searchQuery(q):
        connect = mysql.connect()
        search_cursor = connect.cursor()
        search_cursor.execute("SELECT item_id, item_name, author FROM items \
                WHERE item_name LIKE '%% %s %%' OR author LIKE '%% %s %%'" %(q, q))
        results = search_cursor.fetchall()

        refined_results = {}
        for i, item in enumerate(results):
            refined_results[i] = {
                        "item_id": int(item[0]),
                        "item_name": item[1],
                        "author": item[2]
                    }

        search_cursor.close()
        if len(refined_results) > 20:
            return refined_results

        search_cursor = self.connect.cursor()
        search_cursor.execute("SELECT i.item_id, i.item_name, i.author FROM items i \
                        LEFT JOIN items_categories ic ON i.item_id = ic.item_id \
                        LEFT JOIN categories c ON c.category_id = ic.category_id \
                        WHERE c.category_name LIKE '%% %s %%'" %(q)) 
        results = search_cursor.fetchall()

        i = len(results)
        for item in enumerate(results):
            refined_results[i] = {
                        "item_id": int(item[0]),
                        "item_name": item[1],
                        "author": item[2]
                    }
            i += 1

        return refined_results
