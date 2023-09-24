"""
character_dao.py

This module provides the CharacterDAO class, a stateless
data access object that abstracts and encapsulates interactions
with the MongoDB database for the `Character` model.

All base operations are inherited from BaseDAO class.
"""


from data_access.base_dao import BaseDAO
from data_access.models import Character


class CharacterDAO(BaseDAO[Character]):
    """
    Main class for interactions related to the `Character` model.

    Attributes:
        model: A specific document model to work with
    """
    model = Character
