from data_access.base_dao import BaseDAO
from data_access.models import Character


class CharacterDAO(BaseDAO[Character]):
    model = Character
