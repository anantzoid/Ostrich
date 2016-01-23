from datetime import datetime, timedelta
import random
import string
import pytz
import copy
from operator import itemgetter
from app import webapp
from app import mysql
from flask import make_response, jsonify

'''
Generic helpers
'''
class Utils():
    @staticmethod
    def getAdmins():
        return [1,5,6,8,9,27,28]

    @staticmethod
    def fetchOneAssoc(cursor):
        data = cursor.fetchone()
        if data == None :
            return None
        desc = cursor.description
        datadict = {}

        for (name, value) in zip(desc, data) :
            if isinstance(value, datetime) or isinstance(value, timedelta):
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
        current_timestamp = datetime.now(pytz.timezone('Asia/Calcutta'))
        order_placed = str(current_timestamp).split('.')[0]
        return order_placed

    @staticmethod
    def getDefaultReturnTimestamp(current_timestamp, num_days):
        if isinstance(current_timestamp, str) or isinstance(current_timestamp, unicode):
            current_timestamp = datetime.strptime(current_timestamp, "%Y-%m-%d %H:%M:%S")

        next_week_timestamp = str(current_timestamp + timedelta(days=num_days))
        order_return = next_week_timestamp.split('.')[0]

        return order_return

    @staticmethod
    def getDefaultTimeSlot(interval=6):
        # Get diff all time slots w.r.t to the next 6th hour
        # Check if hour lies within any timeslot
        # check for nearest end time and start time
        # Return the closer option

        current_timestamp = datetime.now(pytz.timezone('Asia/Calcutta'))

        # NOTE temp workaround
        # making next timestamp to nextday afternoon if the order is made latenight
        if current_timestamp.hour >= 19 or current_timestamp.hour < 6:
            return 2 

        next_timestamp = current_timestamp + timedelta(hours=interval)
        next_timestamp = str(next_timestamp.time())
        next_timestamp = datetime.strptime(next_timestamp.split(".")[0], '%H:%M:%S')
      
        from app.models import Order
        time_slots_dirty = Order.getTimeSlot(active=1)
        for slot in time_slots_dirty:
            slot['start_time'] = datetime.strptime(slot['start_time'], '%H:%M:%S')
            slot['end_time'] = datetime.strptime(slot['end_time'], '%H:%M:%S')

            # Checking if new timestamp lies within any given slot
            if slot['start_time'].hour <= next_timestamp.hour and slot['end_time'].hour > next_timestamp.hour:
                return slot['slot_id']

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
                return min_prev_slot['slot_id']

        # Get next immediate time slot
        if next_slots:
            min_next_slot = min(next_slots, key=itemgetter('diff'))
            return min_next_slot['slot_id']
       
        return 2

    @staticmethod
    def getNextTimeslots(start_time, timeslots, num):
        # Sort all start times
        # Find start_time in the sorted list and return the next 2 consecutive ids
        start_time = int(start_time.split(':')[0])
        all_starttime = [(int(ts['start_time'].split(':')[0]), ts) for ts in timeslots]
        all_starttime = sorted(all_starttime, key=itemgetter(0))
        slot_index = [i for i,ts in enumerate(all_starttime) if ts[0] == start_time][0]
        next_slots = []
        for i in range(1,4):
            next_slots.append(all_starttime[(slot_index+i)%len(all_starttime)][1])
        return next_slots
   
    @staticmethod
    def formatTimeSlots(order_timeslots):
        # Mark day
        # Get day of first time slot and the rest will follow suit
        new_timeslots = []
        for i,ts in enumerate(order_timeslots):
            if i == 0:
                if int(ts['start_time'].split(":")[0]) - int(datetime.now(pytz.timezone('Asia/Calcutta')).hour) > 0:
                    start_day = 'Today'
                else:
                    start_day = 'Tomorrow'
                day = start_day
            else:
                if int(ts['start_time'].split(":")[0]) - int(order_timeslots[i-1]['start_time'].split(":")[0]) >= 0:
                    day = start_day
                else:
                    day = Utils.fetchNextDayVerbose(start_day)
                start_day = day

            # Format Timeslots
            formatted_time = Utils.cleanTimeSlot(ts)
            ts['formatted'] = day+' '+formatted_time

            # NOTE creating a new object to avoid pass-by-reference
            new_timeslots.append(copy.copy(ts))
        return new_timeslots

    @staticmethod
    def fetchNextDayVerbose(day):
        if day == 'Today':
            return 'Tomorrow'
        elif day == 'Tomorrow':
            current_timestamp = datetime.now(pytz.timezone('Asia/Calcutta'))
            day_after_tomo = current_timestamp + timedelta(days=2)
            return day_after_tomo.strftime("%A")
        else:
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            return days[days.index(day)+1]

    @staticmethod
    def cleanTimeSlot(ts):
        format_start_time = datetime.strptime(ts['start_time'],"%H:%M:%S").strftime("%I:%M")
        if ":00" in format_start_time:
            format_start_time = format_start_time.replace(":00","")
        format_start_time = format_start_time.strip("0")

        format_end_time = datetime.strptime(ts['end_time'],"%H:%M:%S").strftime("%I:%M %p")
        if ":00" in format_end_time:
            format_end_time = format_end_time.replace(":00","")
        format_end_time = format_end_time.strip("0")

        return format_start_time+' - '+format_end_time

    @staticmethod
    def errorResponse(response_object, error_code=webapp.config['HTTP_STATUS_CODE_ERROR']):
       return make_response(jsonify(response_object), error_code) 

    @staticmethod
    def notifyAdmin(user_id, o_type):
        from app.models import User, Notifications
        notification_data = {
                "notification_id":200,
                "title": "ALERT!! "+o_type+" has been placed",
                }
        admins = Utils.getAdmins()
        if user_id in admins:
            return
        for u_id in admins:
            user = User(u_id,'user_id')
            Notifications(user.gcm_id).sendNotification(notification_data)
        return True


