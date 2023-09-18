from strawberry.types.nodes import SelectedField

from gql.types.character_types import CharacterType
from service.power_handler import PowerHandler
from data_access.character_dao import CharacterDAO
from data_access.models import Character
from utils import utils
from settings import MAX_QUERY_DEPTH


class CharacterHandler:
    dao = CharacterDAO
    power_handler = PowerHandler

    @classmethod
    def _assemble_character(
        cls,
        data: Character,
        selected_fields: list[SelectedField],
        rec_depth: int = 0,
    ) -> CharacterType:
        enemy_ids = [enemy.id for enemy in data.enemies]
        selected_fields = utils.get_selected_complex_fields(selected_fields)

        if 'powers' in selected_fields:
            power_ids = [power.id for power in data.powers]
            powers = cls.power_handler.get_many_by_ids(power_ids)
        else:
            powers = []

        if 'enemies' in selected_fields and rec_depth <= MAX_QUERY_DEPTH:
            enemies_fields = selected_fields['enemies'].selections
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
        enemies_data = cls.dao.get_many_by_ids(enemy_ids)

        enemies = [cls._assemble_character(data, selected_fields, rec_depth) 
                   for data in enemies_data]
        return enemies

    @classmethod
    def get_one_by_id(
        cls, id: str, selected_fields: list[SelectedField]
    ) -> CharacterType | None:
        data = cls.dao.get_one_by_id(id)
        if not data:
            return None

        character = cls._assemble_character(data, selected_fields)
        return character

    @classmethod
    def get_all(
        cls, selected_fields: list[SelectedField]
    ) -> list[CharacterType]:
        data = cls.dao.get_all()

        characters = [cls._assemble_character(entry, selected_fields) for 
                      entry in data]
        return characters
