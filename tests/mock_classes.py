from typing import Generic, TypeVar, Any

from mongoengine import Document

from gql.types.common_types import GQLType


T = TypeVar('T', Document, GQLType)


class MockSelectedField:

    def __init__(
        self,
        name: str,
        selections: list['MockSelectedField'] = None
    ):
        self.name = name
        self.selections = selections or []


class MockInfo:

    def __init__(
        self,
        selected_fields: list[MockSelectedField] = None,
        context: dict[str, Any] = None
    ):
        self.selected_fields = selected_fields or []
        self.context = context or dict()


class BaseMockDataInterface(Generic[T]):

    def __init__(self, data_set: dict[str, T]):
        self.data_set = data_set

    def get_one_by_id(self, id: str, *args) -> T | None:
        return self.data_set.get(id)
    
    def get_many_by_id(self, ids: list[str], *args) -> list[T]:
        return [self.data_set[id] for id in ids if id in self.data_set]
    
    def get_all(self, *args) -> list[T]:
        return list(self.data_set.values())


class MockDAO(BaseMockDataInterface[Document]):
    pass


class MockHandler(BaseMockDataInterface[GQLType]):
    pass
