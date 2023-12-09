from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute

class BaseModel(Model):
    created_at = UTCDateTimeAttribute()
    modified_at = UTCDateTimeAttribute()