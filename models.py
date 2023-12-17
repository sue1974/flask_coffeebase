from flask_mongoengine import MongoEngine
from datetime import datetime

db = MongoEngine()


class Coffee(db.Document):

    cof_id = db.SequenceField(required=True, unique=True)
    cof_user_id = db.IntField()
    cof_date = db.DateTimeField(default=datetime.utcnow)
    cof_payed = db.BooleanField(default=False)


