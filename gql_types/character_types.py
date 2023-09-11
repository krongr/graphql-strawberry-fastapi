from enum import Enum

import strawberry


@strawberry.enum
class RoleEnum(Enum):
    HERO = 'hero'
    VILLIAN = 'villain'
    ANTIHERO = 'antihero'
