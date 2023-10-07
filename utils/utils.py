"""
utils.py

This module provides standalone supportive functions.
For now this is the one and only utils module storing all
utils for the project.
"""


from strawberry.types.nodes import SelectedField
from strawberry.types.info import Info


COMPLEX_FIELDS = ['powers', 'enemies']

def get_primary_selected_fields(info: Info) -> list[SelectedField]:
    """
    Extracts list of field selected for GraphQL query.

    :param info: GraphQL context.

    :return: List of SelectedField objects representing fields
             selected for every type in the query.

    :raise TypeError: Raised if Info object or its attributes have
                      unexpected data type.
    :raise IndexError: Raised if 'selected_fields' attribute is empty.
    :raise AttributeError: Raised if Info object don't have
                           nessary attributes.
    """
    return info.selected_fields[0].selections

def get_selected_complex_fields(
    selected_fields: list[SelectedField]
) -> dict[str, SelectedField]:
    """
    Extracts COMPLEX_FIELDS from list of SelectedField objects.
    This function was designed to prevent the overfetch
    of not-requested fields.

    :param selected_fields: List of SelectedField objects representing
                            fields selected for every type in the query.

    :return: A dict with field names from COMPLEX_FIELDS as keys and
             SelectedField objects for those fields as values.

    :raise TypeError: Raised if selected_fields object is not iterable.
    :raise AttributeError: Raised if selected_fields objects don't have
                           nessary attributes.
    """
    return {f'{entry.name}': entry for entry in selected_fields if 
            entry.name in COMPLEX_FIELDS}
