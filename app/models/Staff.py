# -*- coding: utf-8 -*-
"""Staff models."""

from mongoengine import DynamicDocument
from mongoengine import IntField, StringField

from app import utils


class Staff(DynamicDocument):
    meta = {"collection": "staffs"}

    uid = StringField(primary_key=True, default=utils.get_uuid)
    status = IntField(default=0)
    email = StringField()
