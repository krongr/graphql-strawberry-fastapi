import sqlite3
from abc import ABC, abstractmethod

from db import get_db_handler
from gql_types import Character, Power, AbbreviatedCharacter


def get_power_repository():
    return PowerRepository()

def get_character_repository():
    return CharacterRepository()


class AbstractRepository(ABC):
    @abstractmethod
    def get(self, id):
        raise NotImplementedError
    
    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def save(self, obj):
        raise NotImplementedError

    @abstractmethod
    def delete(self, id):
        raise NotImplementedError

class CharacterRepository(AbstractRepository):
    def __init__(self) -> None:
        self.source = get_db_handler()

    def _get_powers(self, char_id:int)->list[Power]:
        try:
            power_ids_raw = self.source.get_character_power_ids(char_id)
        except sqlite3.Error:
            return []
        power_repo = get_power_repository()
        powers = [power_repo.get(_id[0]) for _id in power_ids_raw]
        return powers

    def _get_enemies(self, char_id:int)->list[Character]:
        try:
            enemy_ids_raw = self.source.get_character_enemy_ids(char_id)
        except sqlite3.Error:
            return []
        enemies = [self._create_abbr_char(_id[0]) for _id in enemy_ids_raw]
        return enemies

    def _create_character(self, entry_raw:tuple[int,str,str,int])->Character:
        char_id = entry_raw[0]
        enemies = self._get_enemies(char_id)
        powers = self._get_powers(char_id)
        char = Character(
            id=str(char_id),
            name=entry_raw[1],
            realName=entry_raw[2],
            powers=powers,
            enemies=enemies,
            role=entry_raw[3],
        )
        return char
    
    def _create_abbr_char(self, char_id)->AbbreviatedCharacter:
        try:
            entry_raw = self.source.get_character_entry(char_id)
        except sqlite3.Error:
            raise

        abbr_character = AbbreviatedCharacter(
            id=str(entry_raw[0]),
            name=entry_raw[1],
            realName=entry_raw[2],
            role=entry_raw[3],
        )
        return abbr_character

    def get(self, char_id:int)->Character:
        try:
            entry_raw = self.source.get_character_entry(char_id)
        except sqlite3.Error:
            raise

        if entry_raw is None:
            return None

        return self._create_character(entry_raw)

    def get_all(self)->list[Character]:
        try:
            all_entries_raw = self.source.get_all_character_entries()
        except sqlite3.Error:
            raise

        return [self._create_character(entry) for entry in all_entries_raw]

    def save(self, name:str, role:int, real_name:str='unknown',
            power_ids:list[int]=(), enemy_ids:list[int]=())->int:
        try:
            char_id = self.source.create_character_entry(name, role, real_name)
        except sqlite3.Error:
            raise

        if len(power_ids) > 0:
            self.source.add_character_powers(char_id, power_ids)
        if len(enemy_ids) > 0:
            self.source.add_character_enemies(char_id, enemy_ids)
        return char_id

    def set_character_powers(self, char_id:int, power_ids:list[int])->bool:
        is_deleted = self.source.delete_character_powers(char_id)
        if is_deleted:
            return self.source.add_character_powers(char_id, power_ids)
        return False

    def set_character_enemies(self, char_id:int, enemy_ids:list[int])->bool:
        is_deleted = self.source.delete_character_enemies(char_id)
        if is_deleted:
            return self.source.add_character_enemies(char_id, enemy_ids)
        return False

    def change_cahracter_role(self, char_id:int, role_id:int)->bool:
        return self.source.change_character_role(char_id, role_id)
    
    def delete(self, char_id:int)->bool:
        return self.source.delete_character_entry(char_id)


class PowerRepository(AbstractRepository):
    def __init__(self) -> None:
        self.source = get_db_handler()

    def _get_users(self, power_id:int)->list[AbbreviatedCharacter]:
        try:
            owner_ids_raw = self.source.get_power_user_ids(power_id)
        except sqlite3.Error:
            return []
        char_repo = get_character_repository()
        users = [char_repo._create_abbr_char(_id[0]) for _id in owner_ids_raw]
        return users
    
    def _create_power(self, entry_raw:tuple[int,str])->Power:
        power_id = entry_raw[0]
        users = self._get_users(power_id)
        power = Power(
            id=power_id,
            name=entry_raw[1],
            users=users,
        )
        return power

    def get(self, power_id:int)->Power:
        try:
            entry_raw = self.source.get_power_entry(power_id)
        except sqlite3.Error:
            raise

        if entry_raw is None:
            return None

        return self._create_power(entry_raw)
    
    def get_all(self)->list[Power]:
        try:
            all_entries_raw = self.source.get_all_power_entries()
        except sqlite3.Error:
            raise
        
        return [self._create_power(entry) for entry in all_entries_raw]
    
    def save(self, name:str, user_ids:list[int]=())->int:
        try:
            power_id = self.source.create_power_entry(name)
        except sqlite3.Error:
            raise

        if len(user_ids) > 0:
            self.source.add_power_users(power_id, user_ids)
        return power_id

    def delete(self, power_id:int)->bool:
        return self.source.delete_power_entry(power_id)
