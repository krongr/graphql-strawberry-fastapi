from typing import Optional
from enum import Enum

import strawberry


@strawberry.enum
class CharacterRole(Enum):
    HERO = 1
    VILLIAN = 2
    ANTIHERO = 3

@strawberry.type
class AbbreviatedCharacter:
    id: strawberry.ID
    name: str
    realName: Optional[str] = 'unknown'
    role: CharacterRole

@strawberry.type
class Character(AbbreviatedCharacter):
    powers: list[Optional['Power']] = ()
    enemies: list[Optional['AbbreviatedCharacter']] = ()

@strawberry.type
class Power:
    id: strawberry.ID
    name: str
    users: list[Optional['AbbreviatedCharacter']]

@strawberry.input
class CharacterInput:
    name: str
    realName: Optional[str] = 'unknown'
    powerIds: list[Optional[strawberry.ID]] = ()
    enemyIds: list[Optional[strawberry.ID]] = ()
    role: CharacterRole

@strawberry.input
class PowerInput:
    name: str
    powerIds: list[Optional[strawberry.ID]] = ()
    userIds: list[Optional[strawberry.ID]] = ()

@strawberry.input
class SetCharacterPowersInput:
    characterId: strawberry.ID
    powerIds: list[strawberry.ID]

@strawberry.input
class SetCharacterEnemiesInput:
    characterId: strawberry.ID
    enemyIds: list[strawberry.ID]
