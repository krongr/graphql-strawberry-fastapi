from typing import Optional

from mongoengine.errors import (
    MongoEngineException, NotUniqueError, FieldDoesNotExist
)

from models import Power
from logger import CustomLogger


logger = CustomLogger('_db_prefill')


class PowerDAO:

    @staticmethod
    def create(name: str, description: Optional[str] = None) -> Power:
        """
        Create and save a new Power document in the database.

        :param name: The name of the power.
        :param description: (Optional) Description for the power.

        :return: The created power object.

        :raises NotUniqueError: If a power with the same 
                                name already exists.
        :raises MongoEngineException: For general database interaction
                                      issues.
        """
        power = Power(name=name)

        # Set the description if provided
        if description:
            power.description = description

        try:
            power.save()
            return power
        except NotUniqueError:
            logger.log_event(
                f'Duplicate power name entry attempt for "{power.name}"'
            )
        except MongoEngineException:
            logger.log_error("DB interaction error")
            raise


    @staticmethod
    def get_by_id(id: str) -> Power | None:
        """
        Retrieve a power by its ID.

        :param id: The ID of the power to retrieve.

        :return: The power object if found, otherwise None.

        :raises MongoEngineException: For general database interaction
                                      issues.
        """
        try:
            return Power.objects(id=id).first()
        except MongoEngineException:
            logger.log_error("DB interaction error")
            raise

    @staticmethod
    def get_by_name_exact(name: str) -> Power | None:
        """
        Retrieve a power by its exact name.

        :param name: The name of the power to retrieve.

        :return: The power object if found, otherwise None.

        :raises MongoEngineException: For general database interaction
                                      issues.
        """
        try:
            return Power.objects(name=name).first()
        except MongoEngineException:
            logger.log_error("DB interaction error")
            raise

    @staticmethod
    def update(power: Power, **kwargs) -> Power:
        """
        Update the attributes of a power with
        the provided key-value pairs.

        :param power: The power object to update.
        :param kwargs: The attributes and their respective values to
                       update the power with.

        :return: The updated power object.

        :raises FieldDoesNotExist: Raised if an attempt is made to
                                   update a field that doesn't exist
                                   in the database schema.
        :raises MongoEngineException: For general database interaction
                                      issues.
        """
        for key, value in kwargs.items():
            setattr(power, key, value)
        
        try:
            power.save()
        except FieldDoesNotExist:
            logger.log_error(
                "Attempt to access a field that is not in the schema"
            )
            raise
        except MongoEngineException:
            logger.log_error("DB interaction error")
            raise
        return power

    @staticmethod
    def search_name_contains(name_part: str) -> list[Power]:
        """
        Search powers whose names contain the given substring.

        :param name_part: A substring to search within power names.

        :return: A list of powers whose names contain
                 the provided substring.
        
        :raises MongoEngineException: For general database interaction
                                      issues.
        """
        try:
            return list(Power.objects(name__icontains=name_part))
        except MongoEngineException:
            logger.log_error("DB interaction error")
            raise

    @staticmethod
    def search_description_contains(description_part: str) -> list[Power]:
        """
        Search powers whose descriptions contain the given substring.

        :param description_part: A substring to search within
                                 power descriptions.

        :return: A list of powers whose descriptions contain
                 the provided substring.

        :raises MongoEngineException: For general database interaction
                                      issues.
        """
        try:
            return list(
                Power.objects(description__icontains=description_part)
            )
        except MongoEngineException:
            logger.log_error("DB interaction error")
            raise

    @staticmethod
    def get_all(page_number=1, page_size=10) -> list[Power]:
        """
        Retrieve a paginated list of all powers.

        :param page_number: The page number to fetch (default is 1).
        :param page_size: The number of powers to retrieve
                          per page (default is 10).

        :return: A list of powers for the specified page.

        :raises MongoEngineException: For general database interaction
                                      issues.
        """
        items_to_skip = page_size * (page_number - 1)
        
        try:
            return list(Power.objects()
                        .order_by('name')
                        .skip(items_to_skip)
                        .limit(page_size))
        except MongoEngineException:
            logger.log_error("DB interaction error")
            raise

    @staticmethod
    def delete(id: str) -> bool:
        """
        Delete a power by its ID.

        :param id: The ID of the power to delete.

        :return: True if the deletion was successful, False otherwise.

        :raises MongoEngineException: For general database interaction
                                      issues.
        """
        try:
            return bool(Power.objects(id=id).delete())
        except MongoEngineException:
            logger.log_error("DB interaction error")
            raise
