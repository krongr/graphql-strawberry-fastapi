"""
power_types.py

This module defines the GraphQL types and inputs related to powers.

Each type or input has fields describing specific attributes or
relationships associated with a power.
"""


from typing import Optional

import strawberry


@strawberry.type
class PowerType:
    """
    GraphQL type representing a power.

    Each power has attributes like an name and description.
    """
    id: strawberry.ID
    name: str
    description: str


@strawberry.input
class PowerInput:
    """
    GraphQL input type for creating a power.

    This input collects information like the power's name and
    description.
    """
    name: str = strawberry.field(
        description='power name (e.g. "flight", "super speed").'
    )
    description: Optional[str] = strawberry.field(
        description=('Power description.'
                     'Defaults to "details unavailable" if not provided.')
    )
