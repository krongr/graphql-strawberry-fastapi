"""
_db_prefill.py

This module contains a script for pre-filling the database from initial data.
The script reads from JSON files and uses DAO objects to populate MongoDB.

Usage:
    python _db_prefill.py

Note:
    This script is intended to be run only once during deployment.
"""


import json
from json.decoder import JSONDecodeError

from mongoengine import connect, disconnect
from mongoengine.errors import MongoEngineException, NotUniqueError

from settings import MONGODB_CONNECTION, PREFILL_FILES
from data_access.character_dao import CharacterDAO
from data_access.power_dao import PowerDAO
from models import Character, Power
from logger import CustomLogger
from exceptions import FileError


logger = CustomLogger('_db_prefill')


def _get_file_data(fpath: str) -> dict:
    """
    Fetch and parse JSON data from a file.

    :param fpath: The path of the file to read.

    :return: A dictionary containing parsed JSON data.

    :raises FileError: Raised when the file either doesn't exist
                       or isn't properly JSON serialized.
    """
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.log_error(f'File does not exist: {fpath}')
        raise FileError(fpath)
    except JSONDecodeError:
        logger.log_error(f'File is not JSON serialized: {fpath}')
        raise FileError(fpath)

def _create_or_retrieve_power(entry: dict) -> Power:
    """
    Create or retrieve a power based on the provided data.

    Tries to create a new power entry using the provided data.
    If a power with the same name already exists in the database,
    it retrieves the existing power entry instead.

    :param entry: A dictionary containing details about the power, 
                  including 'name' and 'description'.

    :return: The created or retrieved power object.

    :raises MongoEngineException: Raised if there's an issue with
                                  the database operation.
    :raises KeyError: Raised if there's a JSON parsing error.
    """
    try:
        power = PowerDAO.create(
            name=entry['name'],
            description=entry['description'],
        )
    except NotUniqueError:
        power = PowerDAO.get_one_by_name_exact(entry['name'])

    return power

def _create_or_retrieve_character(entry: dict, power_ids: dict) -> Character:
    """
    Create or retrieve a character based on the provided data.
    
    Tries to create a new character entry using the provided data.
    If a character with the same alias and name already exists
    in the database, it retrieves the existing character instead.

    :param entry: A dictionary containing details about the character, 
                  including 'alias', 'role', 'name', and 'powers'.
    :param power_ids: Dictionary mapping original power IDs to 
                      database ObjectIds. Used to associate the character 
                      with their powers in the database.

    :return: The created or retrieved character object.

    :raises MongoEngineException: Raised if there's an issue with
                                  the database operation.
    :raises KeyError: Raised if there's a JSON parsing error.
    """
    powers = []
    for _id in entry['powers']:
        try:
            powers.append(power_ids[_id])
        except KeyError:
            logger.log_warning(f'No power record with original ID = {_id}')

    try:
        character = CharacterDAO.create(
            alias=entry['alias'],
            role=entry['role'],
            name=entry['name'],
            powers=powers,
        )
    except NotUniqueError:
        character = CharacterDAO.get_one_by_alias_and_name(
            alias=entry['alias'],
            name=entry['name'],
        )

    return character

def create_characters(power_ids: dict) -> dict:
    """
    Create multiple character entries in the database using
    pre-filled data.
    
    Iterates over the pre-fill character data and tries to create
    each character. If a character with the same alias and name already
    exists, it retrieves the existing character.

    :param power_ids: Dictionary mapping original power IDs to 
                      database ObjectIds. Used to associate characters 
                      with their powers in the database.

    :return: A dictionary where:
             - keys are the original character IDs,
             - values are dictionaries containing:
                 * 'id': The database ObjectId for the character,
                 * 'enemies': A list of original enemy character IDs,
                 * 'object': A reference to the character object.
    
    :raises FileError: Raised when the file either doesn't exist
                       or isn't properly JSON serialized.
    """
    data = _get_file_data(PREFILL_FILES['characters'])
    abbreviated_data = dict()

    for entry in data.values():
        try:
            character = _create_or_retrieve_character(entry, power_ids)
        except KeyError:
            logger.log_error('JSON parsing error')
            logger.log_warning(
                'Failed to create a character: '
                f'{entry.get("alias")} (real name: {entry.get("name")}'
            )
            continue
        except MongoEngineException:
            logger.log_warning(
                'Failed to create a character: '
                f'{entry["alias"]} (real name: {entry["name"]}'
            )
            continue

        abbreviated_data[entry['id']] = {
            'id': character.id,
            'object': character,
            'enemies': entry['enemies'],
        }

    return abbreviated_data

def create_powers() -> dict:
    """
    Create power entries in the database using the pre-fill power data.

    :return: A dictionary mapping original power IDs to their 
             corresponding ObjectId in the database.
    
    :raises FileError: Raised when the file either doesn't exist
                       or isn't properly JSON serialized.
    """
    data = _get_file_data(PREFILL_FILES['powers'])
    power_ids = dict()

    for entry in data.values():
        try:
            power = _create_or_retrieve_power(entry)
        except KeyError:
            logger.log_error('JSON parsing error')
            logger.log_warning(
                f'Failed to create a power: {entry.get("name")}'
            )
            continue
        except MongoEngineException:
            logger.log_warning(
                f'Failed to create a power: {entry["name"]}')
            continue

        power_ids[entry['id']] = power.id

    return power_ids

def add_enemies(character_data: dict) -> None:
    """
    Add enemy references to character entries in the database.

    :param character_data: Dictionary containing character information 
                           including their database ObjectId, 
                           the character object itself, 
                           and a list of enemy IDs.

    :raises KeyError: Raised if there's an unsuited or
                      incorrect dict provided.
    """
    for character in character_data.values():
        enemy_ids = [character_data[_id]['id'] for _id in character['enemies']]
        try:
            CharacterDAO.update(character['object'], enemies=enemy_ids)
        except MongoEngineException:
            logger.log_warning('Failed to add enemies for '
                f'{character["object"].alias} '
                f'(real name: {character["object"].name})'
            )

def run():
    """
    Execute the database pre-fill steps.
    """
    logger.log_event('_db_prefill script started successfully')
    connect(**MONGODB_CONNECTION)

    try:
        power_ids = create_powers()
    except FileError:
        logger.log_warning('Failed to collect power data')
        power_ids = dict()
    
    try:
        character_data = create_characters(power_ids)
    except FileError:
        logger.log_warning('Failed to read file with characters')
        logger.log_event('Script execution stopped due to lac of data')
        disconnect()
        return

    try:
        add_enemies(character_data)
    except KeyError:
        logger.log_error('Unsuited or incorrect character_data dict')
        logger.log_warning('Failed to add character enemies')

    disconnect()
    logger.log_event('_db_prefill script ended as planned')


if __name__ == '__main__':
    run()
