from app import mysql
from app import webapp
from app.models import *

class Arbor():
    @staticmethod
    def getArborBooks(client):
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT * FROM arbor_inventory WHERE in_stock = 1 AND
                 client=%s GROUP BY item_id""", (client.lower(),))
        items = []
        for _ in range(cursor.rowcount):
            item = Utils.fetchOneAssoc(cursor)
            item['arbor_id'] = '_'.join([item['client'], str(item['item_id']), str(item['inventory_id'])])
            item['item'] = WebUtils.extendItemWebProperties([Item(item['item_id']).getObj()])[0]

            categories = []
            for category in item['item']['categories'][:3]:
                categories.append(Item.fetchCategory(name=category)) 
            item['item']['categories'] = categories
            items.append(item)
        return items

    @staticmethod
    def checkout(user_id, arbor_id):
        conn = mysql.connect()
        cursor = conn.cursor()
        
        client, item_id, inv_id = arbor_id.split('_')
        cursor.execute("""SELECT COUNT(*) FROM arbor_inventory WHERE inventory_id =
                %s AND in_stock = 1""", (inv_id,))
        in_stock = cursor.fetchone()[0]

        if not in_stock:
            cursor.execute("""SELECT client, item_id, inventory_id FROM 
            arbor_inventory WHERE client = %s AND item_id = %s AND in_stock = 1""",
            (client, item_id))
            result = cursor.fetchone()
            if result:
                arbor_id = "_".join([str(_) for _ in result])
            else:
                return False

        cursor.execute("""INSERT INTO arbor_orders (user_id, arbor_id) VALUES
                (%s, %s)""", (user_id, arbor_id))
        conn.commit()
        cursor.execute("""UPDATE arbor_inventory SET in_stock = 0 WHERE 
            inventory_id = %s""", (inv_id))
        conn.commit()
        return True
