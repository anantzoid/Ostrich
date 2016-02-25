from app import mysql
from app import webapp
from app.models import Prototype, Utils

class Review(Prototype):
    def __init__(self, review_id):
        self.data = {} 
        self.getData(review_id)

    def getData(self, review_id):
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT * FROM reviews WHERE review_id = %s""",(review_id,))
        self.data = Utils.fetchOneAssoc(cursor)
        cursor.close()

    #TODO transfer to prototype
    def getObj(self):
        obj = vars(self)
        obj = obj['data']
        if not obj:
            obj = None
        return obj

    @staticmethod
    def submitReview(review_data):
        user_id =  Utils.getParam(review_data, 'user_id')
        item_id =  Utils.getParam(review_data, 'item_id')
        order_id =  Utils.getParam(review_data, 'order_id')
        if not(user_id and item_id and order_id):
            return False

        title = Utils.getParam(review_data, 'title')
        description = Utils.getParam(review_data, 'description')
        rating = Utils.getParam(review_data, 'rating')

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO reviews (user_id, item_id, order_id, title, description, rating) VALUES (%s,%s,%s,%s,%s,%s)""",
                (user_id, item_id, order_id, title, description, rating))
        conn.commit()
        review_id = cursor.lastrowid

        #TODO Index item again with review
        return review_id

    def editReview(self, review_data):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO reviews_edit_log (review_id, title, description, rating) VALUES (%s, %s, %s, %s)""",(self.review_id, self.title, self.description, self.rating))
        conn.commit()

        title = Utils.getParam(review_data, 'title')
        description = Utils.getParam(review_data, 'description')
        rating = Utils.getParam(review_data, 'rating')
        
        #TODO delete review if data missing

        cursor.execute("""UPDATE reviews SET title = %s, description = %s, rating = %s, edited = 1, date_edited = CURRENT_TIMESTAMP WHERE review_id = %s""", (title, description, rating, self.review_id))
        conn.commit()
        return True


