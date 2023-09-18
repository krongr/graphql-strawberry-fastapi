from gql.types.character_types import CharacterType
from gql.types.power_types import  PowerType
from service.character_handler import CharacterHandler
from data_access.models import Character
from tests.mock_classes import (
    MockHandler, MockDAO, MockSelectedField
)
from settings import MAX_QUERY_DEPTH


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
        powers=['2'],
        enemies=['1'],
    ),
}

mock_power_types = {
    '1': PowerType(
        id='1',
        name='flight',
        description='Ability to fly',
    ),
    '2': PowerType(
        id='2',
        name='invulnerability',
        description='Ability to withstand enormous amount of damage.'
    ),
}

CharacterHandler.dao = MockDAO(mock_character_docs)
CharacterHandler.power_handler = MockHandler(mock_power_types)

selected_fields ={
    'hollow': [],
    'with_powers': [MockSelectedField('powers')],
    'shallow': [MockSelectedField('enemies')],
    'deep': [
        MockSelectedField(
            'enemies',
            [
                MockSelectedField(
                    'enemies', 
                    [
                        MockSelectedField('powers'),
                    ]
                ),
            ]
        )
    ],
    'exceeding': [
        MockSelectedField(
            'enemies',
            [
                MockSelectedField(
                    'enemies',
                    [
                        MockSelectedField(
                            'enemies',
                            [
                                MockSelectedField(
                                    'enemies',
                                    [
                                        MockSelectedField(
                                            'enemies',
                                            [
                                                MockSelectedField('enemies'),
                                            ]
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        ),
    ],
}


def test_get_one_by_id_valid_id():
    result = CharacterHandler.get_one_by_id(
        id='1',
        selected_fields=selected_fields['hollow'],
    )

    assert isinstance(result, CharacterType)
    assert result.alias == 'Batman'
    assert result.name == 'Bruce Wayne'
    assert result.role == 'hero'
    assert result.enemy_ids == ['2']
    assert result.enemies == []
    assert result.powers == []

def test_get_one_by_id_invalid_id():
    result = CharacterHandler.get_one_by_id(
        id='6',
        selected_fields=selected_fields['hollow'],
    )

    assert result == None

def test_get_one_by_id_with_powers():
    result = CharacterHandler.get_one_by_id(
        id='1',
        selected_fields=selected_fields['with_powers'],
    )

    assert result.alias == 'Batman'
    
    powers = result.powers
    assert isinstance(powers[0], PowerType)
    assert powers[0].name == 'flight'

def test_get_one_by_id_shallow():
    result = result = CharacterHandler.get_one_by_id(
        id='1',
        selected_fields=selected_fields['shallow'],
    )

    assert result.alias == 'Batman'

    enemy = result.enemies[0]
    assert isinstance(enemy, CharacterType)
    assert enemy.alias == 'Joker'
    assert enemy.enemy_ids == ['1']
    assert enemy.enemies == []
    assert enemy.powers == []

def test_get_one_by_id_deep():
    result = CharacterHandler.get_one_by_id(
        id='2',
        selected_fields=selected_fields['deep'],
    )

    assert result.alias == 'Joker'

    enemy = result.enemies[0]
    assert enemy.alias == 'Batman'

    ememy_of_enemy = enemy.enemies[0]
    assert ememy_of_enemy.alias == 'Joker'
    assert ememy_of_enemy.enemy_ids == ['1']
    assert ememy_of_enemy.enemies == []

    deep_powers = ememy_of_enemy.powers
    assert isinstance(deep_powers, list)
    assert deep_powers[0].name == 'invulnerability'
    assert deep_powers[0].description == (
        'Ability to withstand enormous amount of damage.')

def test_get_one_by_id_exceeding():
    assert MAX_QUERY_DEPTH == 4

    result = CharacterHandler.get_one_by_id(
        id='2',
        selected_fields=selected_fields['exceeding'],
    )

    assert result.alias == 'Joker'

    enemy_1 = result.enemies[0]
    assert enemy_1.alias == 'Batman'

    enemy_2 = enemy_1.enemies[0]
    assert enemy_2.alias == 'Joker'

    enemy_3 = enemy_2.enemies[0]
    assert enemy_3.alias == 'Batman'

    enemy_4 = enemy_3.enemies[0]
    assert enemy_4.alias == 'Joker'

    enemy_5 = enemy_4.enemies[0]
    assert enemy_5.alias == 'Batman'
    assert enemy_5.enemies == []
    assert enemy_5.enemy_ids == ['2']

def test_get_all():
    result = CharacterHandler.get_all(
        selected_fields=selected_fields['with_powers'],
    )

    assert isinstance(result, list)
    assert len(result) == 2

    aliases = [character.alias for character in result]
    assert len(aliases) == len(set(aliases))

    character = result[0]
    assert isinstance(character, CharacterType)
    assert character.enemies == []
    assert isinstance(character.powers, list)
    assert isinstance(character.powers[0], PowerType)
