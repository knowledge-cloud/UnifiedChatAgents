from pynamodb.attributes import UnicodeAttribute
from models.base_model import BaseModel


class Client(BaseModel):
    class Meta:
        table_name = 'clients'
        region = 'ap-south-1'
    id = UnicodeAttribute(range_key=True)
    organization_id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    base_url = UnicodeAttribute()

