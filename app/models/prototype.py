from app import webapp

class Prototype():

    def __getattr__(self, field):
        if field in self.data:
            return self.data[field]
        else:
            return None

 
