from models import BaseModel
from pynamodb.attributes import UnicodeAttribute


class Session(BaseModel):
    class Meta:
        table_name = 'sessions'
        region = 'ap-south-1'
    id = UnicodeAttribute(hash_key=True)
    client_id = UnicodeAttribute()