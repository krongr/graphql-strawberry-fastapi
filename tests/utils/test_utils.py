from unittest.mock import Mock

import pytest

from utils import utils


#  Imitates (partly) SelectedField from strawberry.types.nodes
def mock_selected_field(
        name: str, selections: list[Mock] = None
    ) -> Mock:
    selected_field = Mock()
    selected_field.name = name
    selected_field.selections = selections or []
    return selected_field

# Returns list of SelectedField imitations
def mock_query_structure() -> list[Mock]:  
    level_2 = [mock_selected_field(name) for name in 
               ('powers', 'enemies', 'alias')]
    level_1 = [mock_selected_field('character', level_2)]
    return level_1

# Imitates (partly) Info from strawberry.types.info
@pytest.fixture
def mock_info() -> Mock:
    info = Mock()
    info.selected_fields = mock_query_structure()
    return info


def test_get_primary_selected_fields(mock_info):
    result = utils.get_primary_selected_fields(mock_info)

    assert isinstance(result, list)
    assert len(result) == 3
    assert hasattr(result[0], 'selections')

def test_get_selected_complex_fields(mock_info):
    selection = utils.get_primary_selected_fields(mock_info)
    result = utils.get_selected_complex_fields(selection)

    assert isinstance(result, dict)
    assert len(result) == 2
    assert 'powers' in result.keys()
    assert 'enemies' in result.keys()
    assert 'alias' not in result.keys()
    assert hasattr(result['enemies'], 'selections')
    assert isinstance(result['enemies'].selections, list)
