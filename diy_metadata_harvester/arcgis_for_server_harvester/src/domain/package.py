from arcgis_for_server_harvester.src.domain.resource import Resource


class Package:
    def __init__(self, package_id: str) -> None:
        super().__init__()
        self.__package_id: str = package_id
        self.__names_values: dict[str, str] = {}
        self.__resources: dict[str, Resource] = {}

    def get_package_id(self) -> str:
        return self.__package_id

    def set_package_id(self, package_id: str) -> None:
        self.__package_id = package_id

    def add_name_value(self, key: str, value: str) -> None:
        self.__names_values[key] = value

    def add_resource(self, resource: Resource) -> None:
        self.__resources[resource.get_resource_id()] = resource

    def get_package_by_index(self, index: int) -> Resource:
        key: str = list(self.__resources)[index]
        return self.get_resource_by_id(key)

    def get_resource_by_id(self, resource_id: str) -> Resource:
        return self.__resources[resource_id]

    def num_resources(self) -> int:
        return len(self.__resources)

    def to_dict(self, organization_id: str) -> dict:
        result = {'id': self.__package_id, 'owner_org': organization_id}

        for name in self.__names_values:
            result[name] = self.__names_values[name]

        return result