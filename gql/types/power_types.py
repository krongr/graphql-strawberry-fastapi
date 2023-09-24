"""
power_types.py

This module defines all GraphQL types associated
with the power object.
"""


import strawberry

from gql.types.common_types import GQLType


@strawberry.type
class PowerType(GQLType):
    """
    The main type that describes the power and
    includes all its attributes.
    """
    id: strawberry.ID
    name: str
    description: str
