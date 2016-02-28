from app import webapp
from celery import Celery
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from app.scripts.create_celery_app import createCeleryApp
celery = createCeleryApp(webapp)
# NOTE times in crontab are in UTC

'''
    Run everyday at 10am to prompt users to extend the return date if the latter
    is 3 days later 
'''
@periodic_task(run_every=(crontab(hour="04", minute="30")))
def returnDateExtensionReminder():
    from app.scripts.return_date_extension_reminder import returnDateExtensionReminder
    returnDateExtensionReminder()

'''
    Run everyday at 6pm to prompt users to give a pickup time for the order
'''
@periodic_task(run_every=(crontab(hour="12", minute="30")))
def pickupTimeSlot():
    from app.scripts.pickup_timeslot import pickupTimeslot
    pickupTimeslot()

'''
    Run everyday at 7am to show all pickups/deliveries for the day
'''
@periodic_task(run_every=(crontab(hour="01", minute="30")))
def pickupSchedule():
    from app.scripts.pickup_schedule import pickupSchedule
    pickupSchedule()

'''
    Get similar items for all ordered items
'''
@periodic_task(run_every=(crontab(hour="23", minute="30")))
def getRelatedItems():
    from app.scripts.related_items import getRelatedItems
    from app import mysql
    from datetime import datetime
    cursor = mysql.connect().cursor()
    cursor.execute("""SELECT oh.item_id FROM orders o
            INNER JOIN order_history oh ON o.order_id = oh.order_id
            WHERE DATE(o.order_placed) = %s AND 
            o.order_id NOT IN  (SELECT DISTINCT parent_id FROM orders)""",
            (str(datetime.now().date()),)) 
    item_ids = cursor.fetchall()
    for item_id in item_ids:
        getRelatedItems(int(item_id[0]))
