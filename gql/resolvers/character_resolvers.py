from typing import Optional

import strawberry
from strawberry.types.info import Info

from gql.types.character_types import CharacterType
from exceptions import ErrorResponse


@strawberry.type
class CharacterQuery:

    @strawberry.field
    def character(self, info: Info, id: strawberry.ID) -> CharacterType:
        handler = info.context['character_handler']
        character = handler.get_one(id)

        if not character:
            raise ErrorResponse('Character not found!', 404)
        return character

    @strawberry.field
    def allCharacters(self, info) -> list[CharacterType]:
        handler = info.context['character_handler']
        all_characters = handler.get_all()

        return all_characters
