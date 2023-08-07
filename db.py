import sqlite3
from typing import Optional, Any

import config


def get_db_handler():
    return DBHandler()

class DBConnector:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.execute("PRAGMA foreign_keys = ON")
        return self.conn

    def __exit__(self, type, value, traceback):
        self.conn.close()

class DBHandler:
    """
    A handler for database interactions related to characters,
        their powers, roles, and enemies.
    """
    def __init__(self)->None:
        self.connector = DBConnector(config.DB_NAME)

    def _execute_one(self, query:str, params:tuple[Any]=())->int:
        with self.connector as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(query, params)
                connection.commit()
                return cursor.lastrowid
            except sqlite3.Error:
                connection.rollback()
                raise

    def _execute_many(self, query:str, params:list[tuple[Any]]=())->bool:
        with self.connector as connection:
            cursor = connection.cursor()
            try:
                cursor.executemany(query, params)
                connection.commit()
            except sqlite3.Error:
                connection.rollback()
                raise

    def _fetch_one(self, query:str, params:tuple[Any]=())->Optional[tuple[Any]]:
        with self.connector as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(query, params)
                return cursor.fetchone()
            except sqlite3.Error:
                connection.rollback()
                raise

    def _fetch_many(self, query:str, params:tuple[Any]=())->tuple[tuple[Any]]:
        with self.connector as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(query, params)
                return cursor.fetchall()
            except sqlite3.Error:
                connection.rollback()
                raise

    def create_character_entry(self, name:str, role:int,
            real_name:str='unknown')->int:
        query = """
            INSERT INTO characters (name, real_name, role)
            VALUES (?, ?, ?)
        """
        params = (name, real_name, role)
        try:
            char_id = self._execute_one(query, params)
            return char_id
        except sqlite3.Error as err:
            print("Failed to create character:", err)
            raise

    def create_power_entry(self, name:str)->int:
        query = """
            INSERT INTO powers (name)
            VALUES (?)
        """
        params = (name,)
        try:
            power_id = self._execute_one(query, params)
            return power_id
        except sqlite3.Error as err:
            print("Failed to create power:", err)
            raise

    def add_character_powers(self, char_id:int, power_ids:list[int])->bool:
        query = """
            INSERT INTO character_powers (character_id, power_id)
            VALUES (?, ?)
        """
        params = [(char_id, power) for power in power_ids]
        try:
            self._execute_many(query, params)
            return True
        except sqlite3.Error as err:
            print("Failed to add powers "
                f"(char_id={char_id}, power_ids={power_ids}):", err)
            return False

    def add_character_enemies(self, char_id:int, enemy_ids:list[int])->bool:
        query = """
            INSERT INTO character_enemies (character_id, enemy_id)
            VALUES (?, ?)
        """
        params = [(char_id, enemy) for enemy in enemy_ids]
        try:
            self._execute_many(query, params)
            return True
        except sqlite3.Error as err:
            print("Failed to add enemies "
                f"(char_id={char_id}, enemy_ids={enemy_ids}):", err)
            return False

    def add_power_users(self, power_id:int, char_ids:list[int])->bool:
        query = """
            INSERT INTO character_powers (character_id, power_id)
            VALUES (?, ?)
        """
        params = [(char, power_id) for char in char_ids]
        try:
            self._execute_many(query, params)
            return True
        except sqlite3.Error as err:
            print("Failed to add power users "
                f"(power_id={power_id}, char_ids={char_ids}):", err)
            return False

    def get_character_entry(self, char_id:int)->Optional[tuple[int,str,str,int]]:
        query = """
            SELECT *
            FROM characters
            WHERE id = (?)
        """
        params = (char_id,)
        try:
            return self._fetch_one(query, params)
        except sqlite3.Error as err:
            print(f"Failed to collect charecter entry (id={char_id}):", err)
            raise

    def get_power_entry(self, power_id:int)->Optional[tuple[int,str]]:
        query = """
            SELECT *
            FROM powers
            WHERE id = (?)
        """
        params = (power_id,)
        try:
            return self._fetch_one(query, params)
        except sqlite3.Error as err:
            print(f"Failed to collect power (id={power_id}):", err)
            raise

    def get_character_power_ids(self, char_id:int)->tuple[tuple[int]]:
        query = """
            SELECT power_id
            FROM character_powers
            WHERE character_id = (?)
        """
        params = (char_id,)
        try:
            return self._fetch_many(query, params)
        except sqlite3.Error as err:
            print(f"Failed to collect powers (char_id={char_id}):", err)
            raise

    def get_character_enemy_ids(self, char_id:int)->tuple[tuple[int]]:
        query = """
            SELECT enemy_id
            FROM character_enemies
            WHERE character_id = (?)
        """
        params = (char_id,)
        try:
            return self._fetch_many(query, params)
        except sqlite3.Error as err:
            print(f"Failed to collect enemies (char_id={char_id}):", err)
            raise

    def get_power_user_ids(self, power_id:int)->tuple[tuple[int]]:
        query = """
            SELECT character_id
            FROM character_powers
            WHERE power_id = (?)
        """
        params = (power_id,)
        try:
            return self._fetch_many(query, params)
        except sqlite3.Error as err:
            print(f"Failed to collect power users (power_id={power_id}):", err)
            raise

    def get_all_character_entries(self)->tuple[tuple[int,str,str,int]]:
        query = "SELECT * FROM characters"
        try:
            return self._fetch_many(query)
        except sqlite3.Error as err:
            print("Failed to collect charecters:", err)
            raise

    def get_all_power_entries(self)->tuple[tuple[int,str]]:
        query = "SELECT * FROM powers"
        try:
            return self._fetch_many(query)
        except sqlite3.Error as err:
            print("Failed to collect powers:", err)
            raise

    def get_all_roles(self)->tuple[tuple[int,str]]:
        query = "SELECT * FROM character_roles"
        try:
            return self._fetch_many(query)
        except sqlite3.Error as err:
            print("Failed to collect roles:", err)
            raise

    def change_character_role(self, char_id:int, role_id:int)->bool:
        query = """
            UPDATE characters
            SET role = (?)
            WHERE id = (?)
        """
        params = (role_id, char_id)
        try:
            self._execute_one(query, params)
            return True
        except sqlite3.Error as err:
            print(f"Failed to change character role (id={char_id}):", err)
            return False

    def delete_character_entry(self, char_id:int)->bool:
        query = """
            DELETE
            FROM characters
            WHERE id = (?)
        """
        params = (char_id,)
        try:
            self._execute_one(query, params)
            return True
        except sqlite3.Error as err:
            print(f"Failed to delete character (char_id={char_id}):", err)
            return False

    def delete_power_entry(self, power_id:int)->bool:
        query = """
            DELETE
            FROM powers
            WHERE id = (?)
        """
        params = (power_id,)
        try:
            self._execute_one(query, params)
            return True
        except sqlite3.Error as err:
            print(f"Failed to delete power (power_id={power_id}):", err)
            return False

    def delete_character_powers(self, char_id:int)->bool:
        query = """
            DELETE
            FROM character_powers
            WHERE character_id = (?)
        """
        params = (char_id,)
        try:
            self._execute_one(query, params)
            return True
        except sqlite3.Error as err:
            print(f"Failed to delete powers (char_id={char_id}):", err)
            return False

    def delete_character_enemies(self, char_id:int)->bool:
        query = """
            DELETE
            FROM character_enemies
            WHERE character_id = (?)
        """
        params = (char_id,)
        try:
            self._execute_one(query, params)
            return True
        except sqlite3.Error as err:
            print(f"Failed to delete enemies (char_id={char_id}):", err)
            return False
