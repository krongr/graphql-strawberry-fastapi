import strawberry
from strawberry.fastapi import GraphQLRouter

import service


@strawberry.type
class Query:
    @strawberry.field
    def hello(self, name: str = "World") -> str:
        return f"Hello {name}!"


gql_router = GraphQLRouter(
    schema=strawberry.Schema(query=Query),
    context_getter=lambda: {
            "character_handler": service.get_character_handler(),
            "power_handler": service.get_power_handler()
        }
)
