from typing import Generic, TypeVar

from mongoengine.errors import MongoEngineException

from data_access.models import Character, Power
from logger import CustomLogger


T = TypeVar('T', Character, Power)
logger = CustomLogger('data_access.character_dao')


class BaseDAO(Generic[T]):
    model = None

    @classmethod
    def get_one_by_id(cls, id: str) -> T | None:
        if not cls.model:
            raise ValueError("Model not set for this DAO.")

        try:
            return cls.model.objects(id=id).first()
        except MongoEngineException:
            logger.log_error("DB interaction error")
            raise

    @classmethod
    def get_many_by_ids(cls, ids: list[str]) -> list[T]:
        if not cls.model:
            raise ValueError("Model not set for this DAO.")

        try:
            return list(cls.model.objects(id__in=ids))
        except MongoEngineException:
            logger.log_error("DB interaction error")
            raise

    @classmethod
    def get_all(cls) -> list[T]:
        if not cls.model:
            raise ValueError("Model not set for this DAO.")
        
        try:
            return list(cls.model.objects())
        except MongoEngineException:
            logger.log_error("DB interaction error")
            raise
