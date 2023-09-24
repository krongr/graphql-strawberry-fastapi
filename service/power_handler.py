"""
power_handler.py

This module acts as an intermediary, providing stateless methods to
facilitate the interaction between GraphQL resolvers and the DAO layer
related to the Power domain.
It ensures proper data transformation and integrity when
moving between these layers.
"""


from gql.types.power_types import PowerType
from data_access.power_dao import PowerDAO
from data_access.models import Power


class PowerHandler:
    """
    Service layer responsible for orchestrating operations related to
    the Power domain.

    Attributes:
        dao: A reference to the data access class responsible 
             for direct interactions with the database.
    """
    dao = PowerDAO

    @classmethod
    def _assemble_power(cls, data: Power) -> PowerType:
        """
        A supportive method used for PowerType object creation.

        :param data: Power model object from MongoDB.

        :return: Composed PowerType object.
        """
        power = PowerType(
            id=data.id,
            name=data.name,
            description=data.description,
        )
        return power

    @classmethod
    def get_one_by_id(cls, id: str) -> PowerType | None:
        """
        Create a PowerType from MongoDB power document
        fetched by provided ID.

        :param id: ObjectID of a power document in MongoDB.

        :return: PowerType or None if there is no document
                 with provided ID.
        """
        data = cls.dao.get_one_by_id(id)
        if not data:
            return None

        power = cls._assemble_power(data)
        return power

    @classmethod
    def get_many_by_ids(cls, ids: list[str]) -> list[PowerType]:
        """
        Create PowerTypes from MongoDB power documents
        fetched by provided IDs. This method is designed to be used
        from CharacterHandler class to create all powers relevat to
        specific character.

        :param ids: List of ObjectIDs of powers in MongoDB.

        :return: List of PowerTypes. List will be empty if
                 there are no power documents with provided IDs.
        """
        data = cls.dao.get_many_by_ids(ids)

        powers = [cls._assemble_power(entry) for entry in data]
        return powers

    @classmethod
    def get_all(cls) -> list[PowerType]:
        """
        Create PowerType for every power document in MongoDB.

        :return: List of PowerTypes. List will be empty if
                 there are no power documents.
        """
        data = cls.dao.get_all()

        powers = [cls._assemble_power(entry) for entry in data]
        return powers
