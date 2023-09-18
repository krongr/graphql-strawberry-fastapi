from gql.types.power_types import PowerType
from data_access.power_dao import PowerDAO
from data_access.models import Power


class PowerHandler:
    dao = PowerDAO

    @classmethod
    def _assemble_power(cls, data: Power) -> PowerType:
        power = PowerType(
            id=data.id,
            name=data.name,
            description=data.description,
        )
        return power

    @classmethod
    def get_one_by_id(cls, id: str) -> PowerType | None:
        data = cls.dao.get_one_by_id(id)
        if not data:
            return None

        power = cls._assemble_power(data)
        return power

    @classmethod
    def get_many_by_ids(cls, ids: list[str]) -> list[PowerType]:
        data = cls.dao.get_many_by_ids(ids)

        powers = [cls._assemble_power(entry) for entry in data]
        return powers

    @classmethod
    def get_all(cls) -> list[PowerType]:
        data = cls.dao.get_all()

        powers = [cls._assemble_power(entry) for entry in data]
        return powers
