import datetime
import random
import string
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
    def getDefaultTimeSlot():
        cursor = mysql.connect().cursor()
        cursor.execute("SELECT slot_id FROM time_slots LIMIT 1")
        slot = int(cursor.fetchone()[0])
        return slot

    @staticmethod
    def errorResponse(response_object, error_code=webapp.config['HTTP_STATUS_CODE_ERROR']):
       return make_response(jsonify(response_object), error_code) 
