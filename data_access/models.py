from mongoengine import (
    Document, StringField, ListField, LazyReferenceField, CASCADE
)

from gql.types.character_types import RoleEnum


class Power(Document):
    name = StringField(
        required=True, unique=True, min_length=2, max_length=40
    )
    description = StringField(default='details unavailable', max_length=300)

    meta = {
        'collection': 'powers',
    }

class Character(Document):
    alias = StringField(required=True, min_length=2, max_length=40)
    name = StringField(default='unknown', min_length=2, max_length=40)
    role = StringField(choices=[e.value for e in RoleEnum])
    powers = ListField(
        LazyReferenceField(Power, reverse_delete_rule=CASCADE),
    )
    enemies = ListField(
        LazyReferenceField('Character', reverse_delete_rule=CASCADE),
    )

    meta = {
        'collection': 'characters',
        'indexes': [
            {
                'fields': ['alias', 'name'],
                'unique': True,
            },
        ]
    }
