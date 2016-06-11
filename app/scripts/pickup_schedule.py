import json
from app import mysql
from app import webapp
from app.models import Utils
from app.models import Mailer
from app.models import Order
from app.models import User
from app.models import Lend

def pickupSchedule():
    current_ts = Utils.getCurrentTimestamp()
    date = current_ts.split(' ')[0]

    # Order Pickup
    order_list = []
    cursor = mysql.connect().cursor()
    user_id_format_char = ",".join(["%s"] * len(Utils.getAdmins()))

    cursor.execute("""SELECT COUNT(*) 
        FROM orders
        WHERE DATE(order_return) = %s AND order_id NOT IN
        (SELECT DISTINCT parent_id FROM orders) AND user_id NOT IN ("""+user_id_format_char+""")
        AND order_status >= 4""",
        tuple([date]) +  tuple(Utils.getAdmins()))
    order_ids = cursor.fetchone()
    if order_ids[0] > 0:
        Utils.notifyAdmin(-1, "PICKUPS DUE TODAY!!")

    cursor.execute("""SELECT COUNT(*)
        FROM b2b_users WHERE DATE(timestamp) = %s""", (Utils.getDefaultReturnTimestamp(current_ts, -21).split(' ')[0],))
    order_ids = cursor.fetchone()
    if order_ids[0] > 0:
        Utils.notifyAdmin(-1, "B2B PICKUPS DUE!!")

    return None
