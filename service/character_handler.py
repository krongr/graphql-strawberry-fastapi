"""
character_handler.py

This module acts as an intermediary, providing stateless methods to
facilitate the interaction between GraphQL resolvers and the DAO layer
related to the Character domain.
It ensures proper data transformation and integrity when
moving between these layers.
"""


from strawberry.types.nodes import SelectedField

from gql.types.character_types import CharacterType
from service.power_handler import PowerHandler
from data_access.character_dao import CharacterDAO
from data_access.models import Character
from logger import CustomLogger
from utils import utils
from settings import MAX_QUERY_DEPTH


logger = CustomLogger('service.character_handler')


class CharacterHandler:
    """
    Service layer responsible for orchestrating operations related to
    the Character domain.

    Attributes:
        dao: A reference to the data access class responsible 
             for direct interactions with the database.
        power_handler: A service layer dedicated to operations
                       associated with power types and objects.
                       Essential for processing and resolving
                       references related to powers within the
                       Character domain.
    """
    dao = CharacterDAO
    power_handler = PowerHandler

    @classmethod
    def _assemble_character(
        cls,
        data: Character,
        selected_fields: list[SelectedField],
        rec_depth: int = 0,
    ) -> CharacterType:
        """
        A supportive method used for CharacterType object creation.

        :param data: Character model object from MongoDB.
        :param selected_fields: List of strawberry type SelectedField,
                                representing fields selected for the
                                character via GraphQL query.
        :param rec_depth: Recursion depth flag, used to control
                          self-referensing fields and overal query depth.

        :return: Composed CharacterType object.
        """
        enemy_ids = [enemy.id for enemy in data.enemies]
        try:
            selected_fields = utils.get_selected_complex_fields(
                selected_fields,
            )
        except AttributeError:
            logger.log_error('Failed to process selected fields')
            selected_fields = dict()

        if 'powers' in selected_fields:
            power_ids = [power.id for power in data.powers]
            powers = cls.power_handler.get_many_by_ids(power_ids)
        else:
            powers = []

        if 'enemies' in selected_fields and rec_depth <= MAX_QUERY_DEPTH:
            try:
                enemies_fields = selected_fields['enemies'].selections
            except AttributeError:
                logger.log_error('Failed to process selected fields')
                selected_fields = list()
            enemies = cls._fetch_enemies(
                enemy_ids, enemies_fields, rec_depth+1
            )
        else:
            enemies = []

        character = CharacterType(
            id=data.id,
            alias=data.alias,
            name=data.name,
            role=data.role,
            powers=powers,
            enemies=enemies,
            enemy_ids=enemy_ids,
        )
        return character

    @classmethod
    def _fetch_enemies(
        cls,
        enemy_ids: list[str],
        selected_fields: list[SelectedField],
        rec_depth: int,
    ) -> list[CharacterType]:
        """
        A supportive method used for fetching enemies data and
        creating CharacterType objects from fetched data.

        :param enemy_ids: List of ObjectIDs of Character documents
                          from MongoDB.
        :param selected_fields: List of strawberry type SelectedField,
                                representing fields selected for the
                                character via GraphQL query.
        :param rec_depth: Recursion depth flag, used to control
                          self-referensing fields and overal query depth.

        :return: List of CharacterTypes.
        """
        enemies_data = cls.dao.get_many_by_ids(enemy_ids)

        enemies = [cls._assemble_character(data, selected_fields, rec_depth) 
                   for data in enemies_data]
        return enemies

    @classmethod
    def get_one_by_id(
        cls, id: str, selected_fields: list[SelectedField]
    ) -> CharacterType | None:
        """
        Create a CharacterType from MongoDB character document
        fetched by provided ID.

        :param id: ObjectID of a character document in MongoDB.
        :param selected_fields: List of strawberry type SelectedField,
                                representing fields selected for the
                                character via GraphQL query.

        :return: CharacterType or None if there is no document
                 with provided ID.
        """
        data = cls.dao.get_one_by_id(id)
        if not data:
            return None

        character = cls._assemble_character(data, selected_fields)
        return character

    @classmethod
    def get_all(
        cls, selected_fields: list[SelectedField]
    ) -> list[CharacterType]:
        """
        Create CharacterType for every character document in MongoDB.

        :param selected_fields: List of strawberry type SelectedField,
                                representing fields selected for the
                                character via GraphQL query.

        :return: List of CharacterTypes. List will be empty if
                 there are no character documents.
        """
        data = cls.dao.get_all()

        characters = [cls._assemble_character(entry, selected_fields) for 
                      entry in data]
        return characters
