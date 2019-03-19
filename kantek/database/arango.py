import time

from pyArango import validation
from pyArango.connection import Connection
from pyArango.database import Database
from pyArango.document import Document
from pyArango.theExceptions import DocumentNotFoundError, CreationError
from telethon.tl.types import Chat

import config
from pyArango.collection import Collection, Field
from pyArango.validation import Int, String, NotNull
import config


class Chats(Collection):
    _fields = {
        'id': Field([NotNull(), Int()]),
        'title': Field([NotNull()]),
        'tags': Field([NotNull()])
    }

    _validation = {
        'on_save': True,
        'allow_foreign_fields': False
    }

    _properties = {
        "keyOptions": {
            "allowUserKeys": True
        }
    }

    def add_chat(self, chat: Chat):
        data = {'_key': str(chat.id),
                'id': chat.id,
                'title': chat.title,
                'tags': {}}
        try:
            doc = self.createDocument(data)
            doc.save()
        except CreationError:
            pass


# class Group(Document):


class ArangoDB:
    def __init__(self):
        self.conn = Connection(arangoURL=config.db_host,
                               username=config.db_username,
                               password=config.db_password)
        self.db = self._get_db(config.db_name)
        self.db.dropAllCollections()
        self.groups: Chats = self._get_collection('Chats')
        # self.groups.ensureHashIndex(['id'], unique=True)

    def _get_db(self, db: str) -> Database:
        if self.conn.hasDatabase(db):
            return self.conn[db]
        else:
            return self.conn.createDatabase(db)

    def _get_collection(self, collection: str) -> Collection:
        if self.db.hasCollection(collection):
            return self.db[collection]
        else:
            return self.db.createCollection(collection)