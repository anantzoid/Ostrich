from app import webapp

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
            datadict[name[0]] = value

        return datadict

    @staticmethod
    def getParam(obj, var):
        return obj[var] if var in obj else ''

