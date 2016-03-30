from app import mysql
from app.models import Prototype, Utils

class Collection(Prototype):
    def __init__(self, collection_id):
        self.getData(collection_id)
    
    def getData(self, collection_id):
        cursor = mysql.connect().cursor()
        cursor.execute("""SELECT c.*, 
            (select group_concat(ci.item_id separator ',') from collections_items ci 
            where ci.collection_id = c.collection_id and ci.active = 1) as item_ids,
            (select group_concat(concat(cm.meta_key,":",cm.meta_value) separator '&') from collections_metadata cm 
            where cm.collection_id = c.collection_id) as metadata
            FROM collections c WHERE c.collection_id = %s""", (collection_id,))
        self.data = Utils.fetchOneAssoc(cursor)

        collections_metadata_raw = self.data['metadata']
        self.data['metadata'] = {}
        for props in collections_metadata_raw.split('&'):
            props_formatted = props.split(':')
            self.data['metadata'][props_formatted[0]] = props_formatted[1]
        if not self.data:
            self.data = {}
        
    def getObj(self):
        obj = vars(self)
        obj = obj['data']
        return obj

