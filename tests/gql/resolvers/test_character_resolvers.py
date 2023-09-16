
from unittest.mock import Mock

import pytest

from gql.types.character_types import CharacterType
from gql.resolvers.character_resolvers import CharacterQuery
from exceptions import ErrorResponse


mock_characters = {
    '1': CharacterType(
        id='1',
        alias='Batman',
        name='Bruce Wayne',
        role='hero',
        powers=[],
        enemies=[],
        enemy_ids=[],
    ),
    '2': CharacterType(
        id='2',
        alias='Joker',
        name='unknown',
        role='villain',
        powers=[],
        enemies=[],
        enemy_ids=[],
    ),
}

def mock_get_one(id):
    return mock_characters.get(id)

def mock_get_all():
    return list(mock_characters.values())


@pytest.fixture
def mock_character_handler():
    handler = Mock()
    handler.get_one.side_effect = mock_get_one
    handler.get_all.side_effect = mock_get_all
    return handler

@pytest.fixture
def mock_info(mock_character_handler):
    mock_info = Mock()
    mock_info.context = {'character_handler': mock_character_handler}
    return mock_info


def test_character_valid_id(mock_info):
    result = CharacterQuery().character(
        info=mock_info,
        id='1',
    )
    assert result.alias == 'Batman'
    assert result.enemies == []

def test_character_invalid_id(mock_info):
    with pytest.raises(ErrorResponse) as error:
        result = CharacterQuery().character(
            info=mock_info,
            id='8',
        )

    assert error.value.msg == 'Character not found!'
    assert error.value.code == 404

def test_allCharacters(mock_info):
    result = CharacterQuery().allCharacters(info=mock_info)

    assert type(result) == list
    assert len(result) == 2
    assert type(result[0]) == CharacterType
