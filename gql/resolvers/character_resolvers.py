"""
character_resolvers.py

This module provides the necessary GraphQL queries related to
the Character domain. The actual data processing is delegated to the
'character_handler' which is expected to be provided in
the GraphQL context. 
"""


from typing import Optional

import strawberry
from strawberry.types.info import Info

from gql.types.character_types import CharacterType
from logger import CustomLogger
from utils import utils


logger = CustomLogger('service.character_resolvers')


@strawberry.type
class CharacterQuery:

    @strawberry.field
    def character(
        self, info: Info, id: strawberry.ID
    ) -> Optional[CharacterType]:
        """
        Fetches a single Character entity based on provided ID and
        analysis query.

        :param info: GraphQL context. 
        :param id: ObjectID of a character document in MongoDB.

        :return: CharacterType or None if there is no document
                 with provided ID.
        """
        try:
            selected_fields = utils.get_primary_selected_fields(info)
        except (IndexError, AttributeError, TypeError):
            logger.log_error('Failed to extract selected fields')
            selected_fields = []

        try:
            handler = info.context['character_handler']
        except (KeyError, AttributeError, TypeError):
            logger.log_error('Failed to access handler or it was not provided')
            return None

        character = handler.get_one_by_id(id, selected_fields)
        return character

    @strawberry.field
    def allCharacters(self, info:Info) -> list[CharacterType]:
        """
        Fetches all Character entities while analysing query.

        :param info: GraphQL context. 

        :return: List of CharacterTypes. List will be empty if
                 there are no character documents or failed to
                 access handler.
        """
        try:
            selected_fields = utils.get_primary_selected_fields(info)
        except (IndexError, AttributeError, TypeError):
            logger.log_error('Failed to extract selected fields')
            selected_fields = []
        try:
            handler = info.context['character_handler']
        except (AttributeError, TypeError):
            logger.log_error('Failed to access handler or it was not provided')
            return []

        all_characters = handler.get_all(selected_fields)
        return all_characters
