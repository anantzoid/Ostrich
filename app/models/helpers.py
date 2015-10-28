from app import webapp
import datetime

'''
Generic helpers
'''
class Helpers():
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
    def getParam(obj, var, var_type=None):
        param = obj[var] if var in obj else ''
        if var_type == 'int':
            if not param.isdigit():
                param = ''

        return param
        
    @staticmethod
    def getCurrentTimestamp():
        current_timestamp = datetime.datetime.now()
        order_placed = str(current_timestamp).split('.')[0]

        return order_placed


    @staticmethod
    def getDefaultReturnTimestamp():
        current_timestamp = datetime.datetime.now()
        next_week_timestamp = str(current_timestamp + datetime.timedelta(days=7))
        order_return = next_week_timestamp.split('.')[0]

        return order_return


