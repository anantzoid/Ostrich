from app import mysql
from app.models import Prototype, Utils

class Incentive(Prototype):
    def __init__(self, incentive_id):
        self.getData(incentive_id)

    def getData(self, incentive_id):
        getdata_cursor = mysql.connect().cursor()
        getdata_cursor.execute("SELECT * FROM incentives WHERE incentive_id = %d" % (incentive_id))
        self.data = Utils.fetchOneAssoc(getdata_cursor)

    def fetchNextIncentive(self):
        if self.next_incentive:
            next_incentive = Incentive(self.next_incentive)
            return next_incentive.getObj()
        else:
            self.next_incentive
    
    def getObj(self):
        obj = vars(self)
        obj = obj['data']
        #TODO insert incentive message here
        return obj

    @staticmethod
    def fetchFirstInviteScheme():
        return 1

