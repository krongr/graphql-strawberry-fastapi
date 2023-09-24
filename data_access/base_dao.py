"""
base_dao.py

This module provides the BaseDAO class, a stateless data access object
that defines base interactions with the MongoDB.

The BaseDAO handles simple CRUD operations for all defined Documents.
It is used as a foundation for all specialized DAO classes to reduce
redundancy.
"""


from typing import Generic, TypeVar

from mongoengine.errors import MongoEngineException

from data_access.models import Character, Power
from logger import CustomLogger


T = TypeVar('T', Character, Power)
logger = CustomLogger('data_access.base_dao')


class BaseDAO(Generic[T]):
    """
    Base class for all DAO classes.
    Provides base CRUD operations, regardless the document type.

    Attributes:
        model: A specific document model to work with
    """
    model = None

    @classmethod
    def get_one_by_id(cls, id: str) -> T | None:
        """
        Retrieve an object by its ID.

        :param id: The ID of the object to retrieve.

        :return: The object if found, otherwise None.

        :raise ValueError: If the model is not specified in BaseDAO
                           or its subclasses.
        :raise MongoEngineException: For general database interaction
                                     issues.
        """
        if not cls.model:
            raise ValueError('Model not set for this DAO.')

        try:
            return cls.model.objects(id=id).first()
        except MongoEngineException:
            logger.log_error('DB interaction error')
            raise

    @classmethod
    def get_many_by_ids(cls, ids: list[str]) -> list[T]:
        """
        Retrieve objects by their IDs.

        :param ids: The list of IDs of the objects to retrieve.

        :return: A list of all found objects, or an empty list if
                 none were found.

        :raises ValueError: If the model is not specified in BaseDAO
                            or its subclasses.
        :raises MongoEngineException: For general database interaction
                                      issues.
        """
        if not cls.model:
            raise ValueError('Model not set for this DAO.')

        try:
            return list(cls.model.objects(id__in=ids))
        except MongoEngineException:
            logger.log_error('DB interaction error')
            raise

    @classmethod
    def get_all(cls) -> list[T]:
        """
        Retrieve all objects.

        :return: A list of all objects, or an empty list if
                 there are no corresponding objects.

        :raises ValueError: If the model is not specified in BaseDAO
                            or its subclasses.
        :raises MongoEngineException: For general database interaction
                                      issues.
        """
        if not cls.model:
            raise ValueError('Model not set for this DAO.')
        
        try:
            return list(cls.model.objects())
        except MongoEngineException:
            logger.log_error('DB interaction error')
            raise
