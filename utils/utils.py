from strawberry.types.nodes import SelectedField
from strawberry.types.info import Info


COMPLEX_FIELDS = ['powers', 'enemies']

def get_primary_selected_fields(info: Info) -> list[SelectedField]:
    return info.selected_fields[0].selections

def get_selected_complex_fields(
    selected_fields: list[SelectedField]
) -> dict[str: SelectedField]:
    return {f'{entry.name}': entry for entry in selected_fields if 
            entry.name in COMPLEX_FIELDS}
