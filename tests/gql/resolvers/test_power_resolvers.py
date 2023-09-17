from gql.types.power_types import PowerType
from gql.resolvers.power_resolvers import PowerQuery
from tests.mock_classes import MockHandler, MockInfo


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


mock_power_handler = MockHandler(mock_power_types)
mock_info = MockInfo(
    context = {'power_handler': mock_power_handler}
)


def test_power_valid_id():
    result = PowerQuery().power(
        info=mock_info,
        id='1',
    )
    assert result.name == 'flight'
    assert result.description == 'Ability to fly'

def test_power_invalid_id():
    result = PowerQuery().power(
        info=mock_info,
        id='8',
    )

    assert result == None

def test_allPowers():
    result = PowerQuery().allPowers(info=mock_info)

    assert type(result) == list
    assert len(result) == 2
    assert type(result[0]) == PowerType

    names = [power.name for power in result]
    assert len(names) == len(set(names))
