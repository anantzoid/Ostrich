
class Prototype():

    def __getattr__(self, field):
        if field in self.data:
            return self.data[field]
        else:
            return None

    def getObj(self):
        user_obj = vars(self)
        user_obj = user_obj['data']
        if not user_obj:
            user_obj = None
        return user_obj


