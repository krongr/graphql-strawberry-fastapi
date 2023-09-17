from tests.mock_classes import MockHandler, MockInfo, MockSelectedField

from utils import utils


mock_type_fields = [MockSelectedField(name) for name in
                    ('powers', 'enemies', 'alias')]
mock_info = MockInfo(
    selected_fields=[MockSelectedField('character', mock_type_fields)],
)


def test_get_primary_selected_fields():
    result = utils.get_primary_selected_fields(mock_info)

    assert isinstance(result, list)
    assert len(result) == 3
    assert hasattr(result[0], 'selections')

def test_get_selected_complex_fields():
    selection = utils.get_primary_selected_fields(mock_info)
    result = utils.get_selected_complex_fields(selection)

    assert isinstance(result, dict)
    assert len(result) == 2
    assert 'powers' in result.keys()
    assert 'enemies' in result.keys()
    assert 'alias' not in result.keys()
    assert hasattr(result['enemies'], 'selections')
    assert isinstance(result['enemies'].selections, list)
