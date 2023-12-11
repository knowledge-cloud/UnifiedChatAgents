from enum import Enum
from models import BaseModel
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute 

class Role(Enum):
    CRU = 'COGNITION_REDIRECTION_UNIT'
    RAG = 'RETRIEVAL_AUGMENTED_GENERATION'
    RSA = 'REQUEST_SYNTHESIZER_AGENT'
    RS = 'RESPONSE_SYNTHESIZER'
    USER = 'USER'

class Message(BaseModel):
    class Meta:
        table_name = 'messages'
        region = 'ap-south-1'
    session_id = UnicodeAttribute(hash_key=True)
    created_at = UTCDateTimeAttribute(range_key=True)
    message = UnicodeAttribute()
    role = UnicodeAttribute()