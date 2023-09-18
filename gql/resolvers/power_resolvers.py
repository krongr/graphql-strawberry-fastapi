from typing import Optional

import strawberry
from strawberry.types.info import Info

from gql.types.power_types import PowerType


@strawberry.type
class PowerQuery:

    @strawberry.field
    def power(self, info: Info, id: strawberry.ID) -> Optional[PowerType]:
        handler = info.context['power_handler']
        power = handler.get_one_by_id(id)

        return power

    @strawberry.field
    def allPowers(self, info: Info) -> list[PowerType]:
        handler = info.context['power_handler']
        all_powers = handler.get_all()

        return all_powers
