from typing import TypeVar, Generic, List, Tuple
from pynamodb.models import Model
from pynamodb.attributes import UTCDateTimeAttribute
from datetime import datetime


class BaseModel(Model):
    created_at = UTCDateTimeAttribute()
    modified_at = UTCDateTimeAttribute()


T = TypeVar('T', bound=BaseModel)


class BaseDAO(Generic[T]):
    model: T

    def get(self, hash_key, range_key=None) -> T:
        return self.model.get(hash_key, range_key)

    def save(self, model: T, conditional_operator=None, **expected_values) -> T:
        model.created_at = model.created_at or datetime.now()
        model.modified_at = datetime.now()
        return model.save(conditional_operator, **expected_values)

    def update(self, model: T, actions, conditional_operator=None, **expected_values) -> T:
        model.modified_at = datetime.now()
        return model.update(actions, conditional_operator, **expected_values)

    def batch_write(self, cls: T, models: List[T]) -> List[T]:
        with cls.batch_write() as batch:
            for m in models:
                m.created_at = m.created_at or datetime.now()
                m.modified_at = datetime.now()
                batch.save(m)
        return models

    def batch_get(self, cls: T, items_keys: List[Tuple]) -> List[T]:
        items: List[T] = []
        for item in cls.batch_get(items_keys):
            items.append(item)
        return items
