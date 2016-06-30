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
            cursor.execute("""SELECT inventory_id FROM 
            arbor_inventory WHERE client = %s AND item_id = %s AND in_stock = 1""",
            (client, item_id))
            result = cursor.fetchone()
            if result:
                # TODO test this
                arbor_id = str(result[0])
            else:
                return False

        cursor.execute("""INSERT INTO arbor_orders (user_id, inventory_id) VALUES
                (%s, %s)""", (user_id, inv_id))
        conn.commit()
        cursor.execute("""UPDATE arbor_inventory SET in_stock = 0 WHERE 
            inventory_id = %s""", (inv_id,))
        conn.commit()
        return True

    @staticmethod
    def getInventoryItems(client):
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT ai.*, ao.*, i.item_name, 
            ai.inventory_id as inventory_id, u.name FROM arbor_inventory ai
            INNER JOIN items i ON i.item_id = ai.item_id
            LEFT JOIN arbor_orders ao ON ao.inventory_id = ai.inventory_id 
            LEFT JOIN users u ON u.user_id = ao.user_id
            WHERE client = %s AND date_removed IS NULL
            ORDER BY i.item_name""", (client, ))
        items = []
        for _ in range(cursor.rowcount):
            item = Utils.fetchOneAssoc(cursor)
            item['arbor_id'] = '_'.join([item['client'], str(item['item_id']), str(item['inventory_id'])])
            items.append(item)

        return items


    @staticmethod
    def getUserOrders(user_id):
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT * FROM arbor_orders ao 
            INNER JOIN  arbor_inventory ai ON ai.inventory_id = ao.inventory_id
            WHERE ao.user_id = %s ORDER BY order_placed DESC""", (user_id, ))
        orders = {'reading':[], 'history': []}
        for _ in range(cursor.rowcount):
            item = Utils.fetchOneAssoc(cursor)
            item['arbor_id'] = '_'.join([item['client'], str(item['item_id']), str(item['inventory_id'])])
            item['item'] = WebUtils.extendItemWebProperties([Item(item['item_id']).getObj()])[0]

            if not item['order_returned']:
                orders['reading'].append(item)
            else:
                orders['history'].append(item)
        return orders

    @staticmethod
    def returnBook(user_id, arbor_id):
        conn = mysql.connect()
        cursor = conn.cursor()

        client, item_id, inv_id = arbor_id.split('_')
        cursor.execute("""UPDATE arbor_orders SET order_returned = CURRENT_TIMESTAMP
            WHERE inventory_id = %s""", (inv_id, ))
        conn.commit()
        cursor.execute("""UPDATE arbor_inventory SET in_stock = 1 WHERE 
            inventory_id = %s""", (inv_id,))
        conn.commit()
        return True
