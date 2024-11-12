import json


class Package:
    def __init__(self, package_id: str) -> None:
        super().__init__()
        self.__package_id: str = package_id
        self.__names_values: dict[str, str] = {}

    def get_package_id(self) -> str:
        return self.__package_id

    def set_package_id(self, package_id: str) -> None:
        self.__package_id = package_id

    def add_name_value(self, key: str, value: str) -> None:
        self.__names_values[key] = value

    def to_dict(self, organization_id: str) -> dict:
        result = {'id': self.__package_id}

        for name in self.__names_values:
            result[name] = self.__names_values[name]

        result['owner_org'] = organization_id

        return result