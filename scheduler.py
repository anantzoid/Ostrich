from app import webapp
from celery import Celery
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from app.scripts.create_celery_app import createCeleryApp
celery = createCeleryApp(webapp)

'''
    Run everyday at 10am to prompt users to extend the return date if the latter
    is 3 days later 
'''
@periodic_task(run_every=(crontab(hour="10", minute="0")))
def returnDateExtensionReminder():
    from app.scripts.return_date_extension_reminder import returnDateExtensionReminder
    returnDateExtensionReminder()

'''
    Run everyday at 6pm to prompt users to give a pickup time for the order
'''
@periodic_task(run_every=(crontab(hour="18", minute="0")))
def returnDateExtensionReminder():
    from app.scripts.pickup_timeslot import pickupTimeslot
    pickupTimeslot()

