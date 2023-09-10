from typing import Literal, TypedDict
from services.db import Db
from models.model import Model


Document_Type = Literal["docs", "code", "resources"]
Document = TypedDict(
    'Document', {'user_id': int, 'name': str, 'url': str, 'type': Document_Type})


class Document(Model):  # implement base class Model created_at, updated_at, deleted_at
    table_name = 'documents'

    def __init__(self, user_id: int, name: str, url: str, type: Document_Type, db: Db):
        self.document = {
            'user_id': user_id,
            'name': name,
            'url': url,
            'type': type
        }
        self.db = db

    def save(self):
        values = {
            'user_id': self.user_id,
            'name': self.name,
            'type': self.type,
            'url': self.path,
        }

        ok = self.db.save(self.table_name, values)

        if (ok != True):
            raise Exception('Failed to save document to db')
