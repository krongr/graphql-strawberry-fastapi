"""
models.py

This module defines the data models `Power` and `Character` for
the MongoDB database using the MongoEngine ODM.

- `Power`:
    Represents individual abilities or special skills.
    Each power has a unique name and an optional description.
    The powers are stored in the 'powers' collection.

- `Character`:
    Represents individual characters. Each character has attributes
    like an alias, real name, role, associated powers and
    a list of enemies. The role attribute categorizes characters into
    predefined alignments, such as hero, villain, etc.
    Characters are stored in the 'characters' collection and have
    a unique combination of alias and name.
    The model also maintains references to powers and other characters.

This module plays a critical role in structuring the database schema,
ensuring data integrity, and facilitating efficient data operations.

Note:
- When a power or character is deleted, associated references in
  other documents are also deleted.
- For the 'enemies' field in the Character model, LazyReferenceField is used.
  This means when querying, only the ID of the enemy character will be
  fetched initially. The full enemy object will not be automatically loaded
  unless explicitly dereferenced.
"""


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
