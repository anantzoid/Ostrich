import datetime
import random
import string
from operator import itemgetter
from app import webapp
from app import mysql
from flask import make_response, jsonify

'''
Generic helpers
'''
class Utils():
    @staticmethod
    def fetchOneAssoc(cursor):
        data = cursor.fetchone()
        if data == None :
            return None
        desc = cursor.description
        datadict = {}

        for (name, value) in zip(desc, data) :
            if isinstance(value, datetime.datetime) or isinstance(value, datetime.timedelta):
                value = str(value)
            datadict[name[0]] = value
        return datadict

    @staticmethod
    def getParam(obj, var, var_type=None, default=''):
        param = obj[var] if var in obj else default
        if var_type == 'int' and param != default:
            if not param.isdigit() and not param >= 0:
                param = default
            else:
                param = int(param)
        return param

    @staticmethod
    def generateCode(size=4):
        chars = string.ascii_uppercase + string.ascii_lowercase
        return ''.join(random.choice(chars) for _ in range(size))
        

    @staticmethod
    def getCurrentTimestamp():
        current_timestamp = datetime.datetime.now()
        order_placed = str(current_timestamp).split('.')[0]
        return order_placed

    @staticmethod
    def getDefaultReturnTimestamp(current_timestamp, num_days):
        if isinstance(current_timestamp, str) or isinstance(current_timestamp, unicode):
            current_timestamp = datetime.datetime.strptime(current_timestamp, "%Y-%m-%d %H:%M:%S")

        next_week_timestamp = str(current_timestamp + datetime.timedelta(days=num_days))
        order_return = next_week_timestamp.split('.')[0]

        return order_return

    @staticmethod
    def getDefaultTimeSlot(time):
        # Gets best time slot nearest to the next 6 hours
        # Logic:
        # Calculate the timestamp 6 hours from now
        # Checks if it lies in any given time slots
        # Calcualtes diff between all end times to get the nearest past time
        # slot. If it's less than 30 minutes, choose that time slot.
        # Else, look for nearest next time slot.
        # Return 1st time slot of day by default

        current_timestamp = datetime.datetime.now()
        next_timestamp = current_timestamp + datetime.timedelta(hours=6)
      
        next_timestamp = datetime.datetime.strptime(time, '%H:%M:%S')
        from app.models import Order
        time_slots = Order.getTimeSlot()
        time_slots_dirty = Order.getTimeSlot()
        for slot in time_slots_dirty:
            slot['start_time'] = datetime.datetime.strptime(slot['start_time'], '%H:%M:%S')
            slot['end_time'] = datetime.datetime.strptime(slot['end_time'], '%H:%M:%S')

            # Checking if new timestamp lies within any given slot
            if slot['start_time'].hour <= next_timestamp.hour and slot['end_time'].hour > next_timestamp.hour:
                return [_ for _ in time_slots if _['slot_id'] == slot['slot_id']][0]

        previous_slots = []
        next_slots = []
        for slot in time_slots_dirty:
            prev_diff = next_timestamp - slot['end_time']
            prev_diff_seconds = prev_diff.total_seconds()
            if  prev_diff_seconds >= 0:
                previous_slots.append({
                    'slot_id': slot['slot_id'],
                    'diff': prev_diff_seconds
                    })

            next_diff = slot['start_time'] - next_timestamp
            next_diff_seconds = next_diff.total_seconds()
            if  next_diff_seconds >= 0:
                next_slots.append({
                    'slot_id': slot['slot_id'],
                    'diff': next_diff_seconds
                    })

        # Get previous immediate time slot
        if previous_slots:
            min_prev_slot = min(previous_slots, key=itemgetter('diff'))
            if min_prev_slot['diff'] <= 1800:
                return [_ for _ in time_slots if _['slot_id'] == min_prev_slot['slot_id']][0]

        # Get next immediate time slot
        if next_slots:
            min_next_slot = min(next_slots, key=itemgetter('diff'))
            return [_ for _ in time_slots if _['slot_id'] == min_next_slot['slot_id']][0]
        
        return [_ for _ in time_slots if _['slot_id'] == 1][0]


    @staticmethod
    def errorResponse(response_object, error_code=webapp.config['HTTP_STATUS_CODE_ERROR']):
       return make_response(jsonify(response_object), error_code) 
