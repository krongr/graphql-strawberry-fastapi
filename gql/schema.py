import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.tools import merge_types

import service
from gql.resolvers.character_resolvers import CharacterQuery
from gql.resolvers.power_resolvers import PowerQuery


@strawberry.type
class TestQuery:
    @strawberry.field
    def hello(self, name: str = 'World') -> str:
        return f'Hello {name}!'
    

queries = merge_types('Query', (TestQuery, CharacterQuery, PowerQuery))


gql_router = GraphQLRouter(
    schema=strawberry.Schema(query=queries),
    context_getter=lambda: {
            'character_handler': service.get_character_handler(),
            'power_handler': service.get_power_handler()
        }
)
