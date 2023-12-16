from pynamodb.attributes import UnicodeAttribute
from models import BaseModel, BaseDAO


class Client(BaseModel):
    class Meta:
        table_name = 'clients'
        region = 'ap-south-1'
    id = UnicodeAttribute(hash_key=True)
    organization_id = UnicodeAttribute()
    name = UnicodeAttribute()
    base_url = UnicodeAttribute()
