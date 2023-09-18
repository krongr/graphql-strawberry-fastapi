import strawberry

from gql.types.common_types import GQLType


@strawberry.type
class PowerType(GQLType):
    id: strawberry.ID
    name: str
    description: str
