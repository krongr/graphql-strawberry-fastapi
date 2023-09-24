"""
power_dao.py

This module provides the PowerDAO class, a stateless
data access object that abstracts and encapsulates interactions
with the MongoDB database for the `Power` model.

All base operations are inherited from BaseDAO class.
"""


from data_access.base_dao import BaseDAO
from data_access.models import Power


class PowerDAO(BaseDAO[Power]):
    """
    Main class for interactions related to the `Power` model.

    Attributes:
        model: A specific document model to work with
    """
    model = Power
