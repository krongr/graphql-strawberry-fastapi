"""
power_resolvers.py

This module provides the necessary GraphQL queries related to
the Power domain. The actual data processing is delegated to the
'power_handler' which is expected to be provided in
the GraphQL context. 
"""


from typing import Optional

import strawberry
from strawberry.types.info import Info

from gql.types.power_types import PowerType
from logger import CustomLogger


logger = CustomLogger('service.power_resolvers')


@strawberry.type
class PowerQuery:

    @strawberry.field
    def power(self, info: Info, id: strawberry.ID) -> Optional[PowerType]:
        """
        Fetches a single Power entity based on provided ID.

        :param info: GraphQL context. 
        :param id: ObjectID of a power document in MongoDB.

        :return: PowerType or None if there is no document
                 with provided ID.
        """
        try:
            handler = info.context['power_handler']
        except (KeyError, AttributeError, TypeError):
            logger.log_error('Failed to access handler or it was not provided')
            return None

        power = handler.get_one_by_id(id)
        return power

    @strawberry.field
    def allPowers(self, info: Info) -> list[PowerType]:
        """
        Fetches all Power entities.

        :param info: GraphQL context. 

        :return: List of PowerTypes. List will be empty if
                 there are no power documents or failed to
                 access handler.
        """
        try:
            handler = info.context['power_handler']
        except (KeyError, AttributeError, TypeError):
            logger.log_error('Failed to access handler or it was not provided')
            return []

        all_powers = handler.get_all()
        return all_powers
