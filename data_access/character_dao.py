"""
character_dao.py

This module provides the CharacterDAO class, a data access object
that abstracts and encapsulates interactions with the
MongoDB database for the `Character` model.

The CharacterDAO handles CRUD operations (Create, Read, Update, Delete)
and specific search functionalities like fetching powers
based on name or description patterns. 

For interactions related to the `Character` model, it's recommended
to use CharacterDAO to ensure consistent behavior and error handling.
"""


from typing import Optional

from mongoengine.errors import (
    MongoEngineException, NotUniqueError, FieldDoesNotExist
)

from models import Character
from logger import CustomLogger


logger = CustomLogger('data_access.character_dao')

class CharacterDAO:

    @staticmethod
    def create(
        alias: str,
        role: str,
        name: Optional[str] = None,
        powers: Optional[list] = None,
        enemies: Optional[list] = None,
    ) -> Character:
        """
        Create and save a new Character document in the database.

        :param alias: The character's alias.
        :param role: The role or alignment of the character.
        :param name: (Optional) The character's real name.
        :param powers: (Optional) List of power references associated
                       with the character.
        :param enemies: (Optional) List of enemy character references.

        :return: The saved Character object.

        :raises NotUniqueError: If a character with the same alias and
                                name exists.
        :raises MongoEngineException: For general database interaction
                                      issues.
        """
        powers = powers or []
        enemies = enemies or []

        character = Character(
            alias=alias,
            role=role,
            powers=powers,
            enemies=enemies,
        )

        # Set the name if provided
        if name:
            character.name = name

        try:
            character.save()
            return character
        except NotUniqueError:
            _name = getattr(character, 'name', 'unknown')
            logger.log_event(
                f"Duplicate entry attempt for {alias} (real name: {_name})"
            )
            raise
        except MongoEngineException:
            logger.log_error("DB interaction error")
            raise

    @staticmethod
    def get_by_id(id: str) -> Character | None:
        """
        Retrieve a character by its ID.

        :param id: The ID of the character to retrieve.

        :return: The character object if found, otherwise None.

        :raises MongoEngineException: For general database interaction
                                      issues.
        """
        try:
            return Character.objects(id=id).first()
        except MongoEngineException:
            logger.log_error("DB interaction error")
            raise

    @staticmethod
    def get_by_alias_and_name(alias: str, name: str) -> Character | None:
        """
        Retrieve a character by its alias and name.

        :param alias: The alias of the character to retrieve.
        :param name: The name of the character to retrieve.

        :return: The character object if found, otherwise None.

        :raises MongoEngineException: For general database interaction
                                      issues.
        """
        try:
            return Character.objects(name=name, alias=alias).first()
        except MongoEngineException:
            logger.log_error("DB interaction error")
            raise

    @staticmethod
    def update(character: Character, **kwargs) -> Character:
        """
        Update the attributes of a character with 
        the provided key-value pairs.

        :param character: The character object to update.
        :param kwargs: The attributes and their respective values to
                       update the character with.

        :return: The updated character object.

        :raises FieldDoesNotExist: Raised if an attempt is made to
                                   update a field that doesn't exist
                                   in the database schema.
        :raises MongoEngineException: For general database interaction
                                      issues.
        """
        for key, value in kwargs.items():
            setattr(character, key, value)

        try:
            character.save()
        except FieldDoesNotExist:
            logger.log_error(
                "Attempt to access a field that is not in the schema"
            )
            raise
        except MongoEngineException:
            logger.log_error("DB interaction error")
            raise
        return character

    @staticmethod
    def search_name_exact(name: str) -> list[Character]:
        """
        Search characters by exact name match.

        :param name: The exact name of the character to search.

        :return: A list of characters with the exact name.

        :raises MongoEngineException: For general database interaction
                                      issues.
        """
        try:
            return list(Character.objects(name=name))
        except MongoEngineException:
            logger.log_error("DB interaction error")
            raise

    @staticmethod
    def search_name_contains(name_part: str) -> list[Character]:
        """
        Search characters whose names contain the given substring.

        :param name_part: A substring to search within character names.

        :return: A list of characters whose names contain
                 the provided substring.

        :raises MongoEngineException: For general database interaction
                                      issues.
        """
        try:
            return list(Character.objects(name__icontains=name_part))
        except MongoEngineException:
            logger.log_error("DB interaction error")
            raise

    @staticmethod
    def search_alias_exact(alias: str) -> list[Character]:
        """
        Search characters by exact alias match.

        :param alias: The exact alias of the character to search.

        :return: A list of characters with the exact alias.

        :raises MongoEngineException: For general database interaction
                                      issues.
        """
        try:
            return list(Character.objects(alias=alias))
        except MongoEngineException:
            logger.log_error("DB interaction error")
            raise

    @staticmethod
    def search_alias_contains(alias_part: str) -> list[Character]:
        """
        Search characters whose aliases contain the given substring.

        :param alias_part: A substring to search within character aliases.

        :return: A list of characters whose aliases contain
                 the provided substring.

        :raises MongoEngineException: For general database interaction
                                      issues.
        """
        try:
            return list(Character.objects(alias__icontains=alias_part))
        except MongoEngineException:
            logger.log_error("DB interaction error")
            raise

    @staticmethod
    def get_all(page_number=1, page_size=10) -> list[Character]:
        """
        Retrieve a paginated list of all characters.

        :param page_number: The page number to fetch (default is 1).
        :param page_size: The number of characters to retrieve
                          per page (default is 10).

        :return: A list of characters for the specified page.

        :raises MongoEngineException: For general database interaction
                                      issues.
        """
        items_to_skip = page_size * (page_number - 1)
        
        try:
            return list(Character.objects()
                        .order_by('alias')
                        .skip(items_to_skip)
                        .limit(page_size))
        except MongoEngineException:
            logger.log_error("DB interaction error")
            raise
    
    @staticmethod
    def delete(id: str) -> bool:
        """
        Delete a character by its ID.

        :param id: The ID of the character to delete.

        :return: True if the deletion was successful, False otherwise.

        :raises MongoEngineException: For general database interaction
                                      issues.
        """
        try:
            return bool(Character.objects(id=id).delete())
        except MongoEngineException:
            logger.log_error("DB interaction error")
            raise

    # def _validate_ids(
    #     character_ids: list[str],
    # ) -> tuple[set[str], set[str]]:
    #     valid_ids = set(
    #         [char.id for char in Character.objects(id__in=character_ids)]
    #     )
    #     invalid_ids = set(character_ids).difference(valid_ids)
    #     return valid_ids, invalid_ids

    # @staticmethod
    # def add_enemies(character_id: str, new_enemy_ids: list[str]) -> Character:
    #     character = CharacterDAO.get_by_id(character_id)
    #     enemy_ids = set([enemy.id for enemy in character.enemies])

    #     new_enemy_ids = set(new_enemy_ids).difference(enemy_ids)
    #     if len(new_enemy_ids) < 1:
    #         print('nothing new')
    #         return character
        
    #     (valid_ids, invalid_ids) = (
    #         CharacterDAO._validate_ids(list(new_enemy_ids))
    #     )

    #     enemy_ids = enemy_ids.union(valid_ids)

    #     return (
    #         CharacterDAO._update(character, enemies=list(enemy_ids)),
    #         'some report',
    #     )

    # def get_user_by_email(email):
    #     return User.objects(email=email).first()