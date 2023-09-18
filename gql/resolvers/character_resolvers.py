from typing import Optional

import strawberry
from strawberry.types.info import Info

from gql.types.character_types import CharacterType
from utils import utils


@strawberry.type
class CharacterQuery:

    @strawberry.field
    def character(self, info: Info, id: strawberry.ID) -> Optional[CharacterType]:
        selected_fields = utils.get_primary_selected_fields(info)
        handler = info.context['character_handler']
        character = handler.get_one_by_id(id, selected_fields)

        return character

    @strawberry.field
    def allCharacters(self, info) -> list[CharacterType]:
        selected_fields = utils.get_primary_selected_fields(info)
        handler = info.context['character_handler']
        all_characters = handler.get_all(selected_fields)

        return all_characters
