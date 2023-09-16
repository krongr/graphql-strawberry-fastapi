
from unittest.mock import Mock

import pytest

from gql.types.character_types import CharacterType
from gql.types.power_types import  PowerType
from service.character_handler import CharacterHandler
from data_access.models import Character


mock_character_docs = {
    '1': Character(
        id='1',
        alias='Batman',
        name='Bruce Wayne',
        role='hero',
        powers=['1'],
        enemies=['2'],
    ),
    '2': Character(
        id='2',
        alias='Joker',
        name='unknown',
        role='villain',
        powers=['1'],
        enemies=['1'],
    ),
}

def mock_get_one_by_id(id: str) -> Character | None:
    return mock_character_docs.get(id)

def mock_get_many_by_id(ids: list[str]) -> list[Character]:
    return [mock_character_docs[id] for id in ids if
            id in mock_character_docs.keys()]

def mock_get_all() -> list[Character]:
    return mock_character_docs.values()

@pytest.fixture
def mock_character_dao() -> Mock:
    dao = Mock()
    dao.get_one_by_id.side_effect = mock_get_one_by_id
    dao.get_many_by_ids.side_effect = mock_get_many_by_id
    dao.get_all.side_effect = mock_get_all
    return dao

@pytest.fixture
def mock_info():
    pass

def test_get_one_valid_id(mock_character_dao):
    handler = CharacterHandler
    handler.dao = mock_character_dao

    result = handler.get_one(id='1')

    assert type(result) == CharacterType
    assert result.alias == 'Batman'
    assert result.enemy_ids == ['2']
    assert type(result.enemies) == list
    assert type(result.powers) == list
    assert type(result.enemies[0]) == CharacterType
    assert type(result.powers[0]) == PowerType

def test_get_one_invalid_id(mock_character_dao):
    handler = CharacterHandler
    handler.dao = mock_character_dao

    result = handler.get_one(id='6')

    assert result == None

def test_get_all(mock_character_dao):
    handler = CharacterHandler
    handler.dao = mock_character_dao

    result = handler.get_all()

    assert type(result) == list
    assert type(result[0]) == CharacterType
    assert len(result) == 2

    aliases = [character.alias for character in result]
    assert len(aliases) == len(set(aliases))

    character = result[0]
    assert type(character.enemies) == list
    assert type(character.powers) == list
    assert type(character.enemies[0]) == CharacterType
    assert type(character.powers[0]) == PowerType
