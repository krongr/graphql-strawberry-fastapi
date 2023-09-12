from typing import Optional
from enum import Enum

import strawberry

from gql_types.power_types import PowerType
from settings import RECURSION_DEPTH


@strawberry.enum(description='Represents the alignment of a character.')
class RoleEnum(Enum):
    HERO = 'hero'
    VILLIAN = 'villain'
    ANTIHERO = 'antihero'

@strawberry.type
class CharacterType:
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
        description=('List of character powers IDs. '
                     'Defaults to empty list if not provided.')
    )
    enemyIds: Optional[list[strawberry.ID]] = strawberry.field(
        description=('List of character enemy IDs. '
                     'Defaults to empty list if not provided.')
    )
