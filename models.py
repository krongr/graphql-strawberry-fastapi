from mongoengine import (
    Document, StringField, ListField, ReferenceField, LazyReferenceField,
    CASCADE,
)

from gql_types.character_types import RoleEnum


class Power(Document):
    """
    Represents individual abilities or special skills.

    Each power has a unique name and an optional description.
    """
    name = StringField(
        required=True, unique=True, min_length=2, max_length=40
    )
    description = StringField(default='details unavailable', max_length=300)

    meta = {
        'collection': 'powers',
    }

class Character(Document):
    """
    Represents individual characters.

    Each character has a unique combination of alias and name.
    A character can have multiple powers and can reference other 
    characters as enemies.
    The role attribute defines the character's alignment.
    """
    alias = StringField(required=True, min_length=2, max_length=40)
    name = StringField(default='unknown', min_length=2, max_length=40)
    role = StringField(choices=[e.value for e in RoleEnum])
    powers = ListField(
        ReferenceField(Power, reverse_delete_rule=CASCADE),
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
