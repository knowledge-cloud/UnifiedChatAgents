from pynamodb.attributes import UnicodeAttribute
from models.dynamo_db import BaseModel


class Client(BaseModel):
    class Meta:
        table_name = 'clients'
        region = 'ap-south-1'
    id = UnicodeAttribute(hash_key=True)
    organization_id = UnicodeAttribute()
    name = UnicodeAttribute()
    base_url = UnicodeAttribute()
