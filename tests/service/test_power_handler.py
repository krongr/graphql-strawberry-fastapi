from gql.types.power_types import  PowerType
from service.power_handler import PowerHandler
from data_access.models import Power
from tests.mock_classes import MockDAO


mock_power_docs = {
    '1': Power(
        id='1',
        name='flight',
        description='Ability to fly',
    ),
    '2': Power(
        id='2',
        name='invulnerability',
        description='Ability to withstand enormous amount of damage.'
    ),
}

PowerHandler.dao = MockDAO(mock_power_docs)


def test_get_one_by_id_valid_id():
    result = PowerHandler.get_one_by_id(id='1')

    assert isinstance(result, PowerType)
    assert result.name == 'flight'
    assert result.description == 'Ability to fly'

def test_get_one_by_id_invalid_id():
    result = PowerHandler.get_one_by_id(id='6')

    assert result == None

def test_get_many_by_ids_valid_ids():
    result = PowerHandler.get_many_by_ids(ids=['2', '3'])

    assert isinstance(result, list)
    assert len(result) == 1

    power = result[0]
    assert power.name == 'invulnerability'
    assert power.description == (
        'Ability to withstand enormous amount of damage.')

def test_get_many_by_ids_invalid_ids():
    result = PowerHandler.get_many_by_ids(ids=['3', '5'])

    assert isinstance(result, list)
    assert len(result) == 0

def test_get_all():
    result = PowerHandler.get_all()

    assert isinstance(result, list)
    assert len(result) == 2

    power = result[0]
    assert hasattr(power, 'name')
    assert hasattr(power, 'description')
