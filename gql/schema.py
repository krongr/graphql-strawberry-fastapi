"""
schema.py

This module sets up the GraphQL router for the application.
It merges different GraphQL query resolvers and provides a
unified schema for the app.
The router is configured with context getters to fetch the necessary
services for resolving GraphQL queries.

Classes:
    - TestQuery: A simple GraphQL query for demonstration purposes.


"""


import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.tools import merge_types

import service
from gql.resolvers.character_resolvers import CharacterQuery
from gql.resolvers.power_resolvers import PowerQuery


@strawberry.type
class TestQuery:
    """
    A simple GraphQL query mostly for health checks.
    Can be omited or removed in future versions.
    """
    @strawberry.field
    def hello(self, name: str = 'World') -> str:
        return f'Hello {name}!'
    

# Merging individual GraphQL query, mutation and subscription resolvers
# to create a unified set.
queries = merge_types('Query', (TestQuery, CharacterQuery, PowerQuery))


# Setting up the GraphQL router with the merged queries and
# configuring context to provide necessary handlers.
gql_router = GraphQLRouter(
    schema=strawberry.Schema(query=queries),
    # Providing the necessary handlers as context for GraphQL resolvers.
    context_getter=lambda: {
            'character_handler': service.get_character_handler(),
            'power_handler': service.get_power_handler()
        }
)
