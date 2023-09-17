from gql.types.character_types import CharacterType
from gql.resolvers.character_resolvers import CharacterQuery
from tests.mock_classes import MockHandler, MockInfo, MockSelectedField


mock_character_types = {
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


mock_character_handler = MockHandler(mock_character_types)
mock_info = MockInfo(
    selected_fields=[MockSelectedField('character')],
    context = {'character_handler': mock_character_handler}
)


def test_character_valid_id():
    result = CharacterQuery().character(
        info=mock_info,
        id='1',
    )

    assert result.alias == 'Batman'
    assert result.enemies == []

def test_character_invalid_id():
    result = CharacterQuery().character(
        info=mock_info,
        id='8',
    )

    assert result == None

def test_allCharacters():
    result = CharacterQuery().allCharacters(info=mock_info)

    assert isinstance(result, list)
    assert len(result) == 2
    assert isinstance(result[0], CharacterType)

    aliases = [character.alias for character in result]
    assert len(aliases) == len(set(aliases))
