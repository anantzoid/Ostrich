from app import mysql
from app import webapp
from app.decorators import async

class Wallet():
    @staticmethod
    @async
    def creditTransaction(wallet_id, user_id, source, source_id,
            amount=webapp.config['DEFAULT_WALLET_CREDIT_AMOUNT']):
        #TODO source, source_id etc validation
        if not wallet_id:
            query = "INSERT INTO user_wallet (amount, user_id) VALUES (%d, %d)"
        else:
            query = "UPDATE user_wallet SET amount = amount + %d WHERE user_id = %d"

        conn = mysql.connect()
        wallet_cursor = conn.cursor()
        wallet_cursor.execute(query % (amount, user_id))
        conn.commit()
        
        Wallet.logTransaction(user_id, 'credit', amount, source, source_id)
        return True

    @staticmethod
    @async
    def debitTransaction(wallet_id, user_id, source, source_id, amount):
        if not wallet_id:
            return False
        else:
            query = "UPDATE user_wallet SET amount = amount - %s WHERE user_id = %s"

        conn = mysql.connect()
        wallet_cursor = conn.cursor()
        wallet_cursor.execute(query, (amount, user_id))
        conn.commit()
        
        Wallet.logTransaction(user_id, 'debit', amount, source, source_id)
        return True

    @staticmethod
    def logTransaction(user_id, transaction_type, amount, source, source_id):
        conn = mysql.connect()
        wallet_cursor = conn.cursor()
        wallet_cursor.execute("""INSERT INTO wallet_transactions (user_id, transaction_type,
                amount, source_type, source_id) VALUES (%s, %s, %s, %s, %s)""", 
                (user_id, transaction_type, amount, source, source_id))
        conn.commit()


