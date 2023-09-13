"""
character_types.py

This module defines the GraphQL types and inputs related to characters.

Each type or input has fields describing specific attributes or
relationships associated with a character, such as
their powers, enemies or role.
"""


from typing import Optional
from enum import Enum

import strawberry

from gql_types.power_types import PowerType
from settings import RECURSION_DEPTH


@strawberry.enum(description='Represents the alignment of a character.')
class RoleEnum(Enum):
    """
    Enum representing the possible roles or alignments
    a character can have.
    """
    HERO = 'hero'
    VILLIAN = 'villain'
    ANTIHERO = 'antihero'

@strawberry.type
class CharacterType:
    """
    GraphQL type representing a character.

    Each character has attributes like an alias, real name, role,
    powers and enemies. Depending on the query depth, `enemies`
    may return full character objects or just IDs.
    """
    id: strawberry.ID
    alias: str = strawberry.field(
        description='Character alias (e.g. Batman, Joker).'
    )
    realName: str = strawberry.field(description='Character real name.')
    role: RoleEnum = strawberry.field(description='Character role.')
    powers: list[PowerType] = strawberry.field(
        description='List of character powers.'
    )
    enemies: list['CharacterType'] | list[strawberry.ID] = strawberry.field(
        description=('List of character enemies. '
                     'And list of enemy IDs, if query exceeds '
                    f'a depth level of {RECURSION_DEPTH}.')
    )
    enemy_ids: list[strawberry.ID] = strawberry.field(
        description='List of character enemy IDs.'
    )

@strawberry.input
class CharacterInput:
    """
    GraphQL input type for creating a character.

    This input collects information like the character's alias,
    real name, role, associated power IDs and enemy IDs.
    """
    alias: str = strawberry.field(
        description='Character alias (e.g. Batman, Joker).'
    )
    realName: Optional[str] = strawberry.field(
        description=('Character real name.'
                     'Defaults to "unknown" if not provided.')
    )
    role: RoleEnum = strawberry.field(
        description=('Character role. '
                     'Can be one of 3: hero, villain or antihero.')
    )
    powerIds: Optional[list[strawberry.ID]] = strawberry.field(
        description=('List of powers IDs that will be assigned to the '
                     'character. Defaults to empty list if not provided.')
    )
    enemyIds: Optional[list[strawberry.ID]] = strawberry.field(
        description=('List of character IDs that will be added as enemies '
                     'to the character. '
                     'Defaults to empty list if not provided.')
    )

@strawberry.input
class CharacterEnemiesInput:
    """
    GraphQL input type for making changes to a character's enemy list.

    This input requires ID of the affected character and
    list of enemy IDs.
    """
    characterId: strawberry.ID = strawberry.field(
        description='ID of a character which enemies you want to change.'
    )
    enemyIds: list[strawberry.ID] = strawberry.field(
        description='List of character IDs.'
    )

@strawberry.input
class CharacterPowersInput:
    """
    GraphQL input type for making changes to a character's power list.

    This input requires ID of the affected character and
    list of power IDs.
    """
    characterId: strawberry.ID = strawberry.field(
        description='ID of a character which powers you want to change.'
    )
    powerIds: list[strawberry.ID] = strawberry.field(
        description='List of powers IDs.'
    )
