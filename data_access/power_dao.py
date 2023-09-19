from data_access.base_dao import BaseDAO
from data_access.models import Power


class PowerDAO(BaseDAO[Power]):
    model = Power
