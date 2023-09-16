
from unittest.mock import Mock

import pytest

from gql.types.power_types import PowerType
from gql.resolvers.power_resolvers import PowerQuery
from exceptions import ErrorResponse


mock_powers = {
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

def mock_get_one(id: str) -> PowerType | None:
    return mock_powers.get(id)

def mock_get_all() -> list[PowerType]:
    return list(mock_powers.values())

@pytest.fixture
def mock_power_handler() -> Mock:
    handler = Mock()
    handler.get_one.side_effect = mock_get_one
    handler.get_all.side_effect = mock_get_all
    return handler

@pytest.fixture
def mock_info(mock_power_handler) -> Mock:
    mock_info = Mock()
    mock_info.context = {'power_handler': mock_power_handler}
    return mock_info


def test_power_valid_id(mock_info):
    result = PowerQuery().power(
        info=mock_info,
        id='1',
    )
    assert result.name == 'flight'
    assert result.description == 'Ability to fly'

def test_power_invalid_id(mock_info):
    with pytest.raises(ErrorResponse) as error:
        result = PowerQuery().power(
            info=mock_info,
            id='8',
        )

    assert error.value.msg == 'Power not found!'
    assert error.value.code == 404

def test_allPowers(mock_info):
    result = PowerQuery().allPowers(info=mock_info)

    assert type(result) == list
    assert len(result) == 2
    assert type(result[0]) == PowerType

    names = [power.names for power in result]
    assert len(names) == len(set(names))
