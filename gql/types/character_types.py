"""
character_types.py

This module defines all GraphQL types associated
with the character object.
"""


from enum import Enum

import strawberry

from gql.types.common_types import GQLType
from gql.types.power_types import PowerType
from settings import MAX_QUERY_DEPTH


@strawberry.enum(description='Represents the alignment of a character.')
class RoleEnum(Enum):
    HERO = 'hero'
    VILLAIN = 'villain'
    ANTIHERO = 'antihero'


@strawberry.type
class CharacterType(GQLType):
    """
    The main type that describes the character and
    includes all its attributes.
    """
    id: strawberry.ID
    alias: str = strawberry.field(
        description='Character alias (e.g. Batman, Joker).'
    )
    name: str = strawberry.field(description='Character real name.')
    role: RoleEnum = strawberry.field(description='Character role.')
    powers: list[PowerType] = strawberry.field(
        description='List of character powers.'
    )
    enemies: list['CharacterType'] = (
        strawberry.field(
            description=(
                'List of character enemies. Will be empty, if query '
                f'exceeds a depth level of {MAX_QUERY_DEPTH}.'
            )
        )
    )
    enemy_ids: list[strawberry.ID] = strawberry.field(
        description='List of character enemy IDs.'
    )
