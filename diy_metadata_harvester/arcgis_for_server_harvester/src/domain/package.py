from arcgis_for_server_harvester.src.domain.resource import Resource


class Package:
    def __init__(self, package_id: str|None, package_name: str) -> None:
        """Package constructor. Package ID should be None when creating a new package from scratch. Package ID cannot
        be None when reading an existing package from CKAN for update or delete. Package name cannot be None and
        should contain a hash of the URL of the ArcGIS for Server service which the package relates to. """
        super().__init__()
        self.__package_id: str = package_id
        self.__package_name: str = package_name
        self.__names_values: dict[str, str] = {}
        self.__resources: dict[str, Resource] = {}

    def get_package_id(self) -> str:
        return self.__package_id

    def set_package_id(self, package_id: str) -> None:
        self.__package_id = package_id

    def get_package_name(self) -> str:
        return self.__package_name

    def set_package_name(self, package_name: str) -> None:
        self.__package_name = package_name

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
        result = {'name': self.__package_name}

        """Package ID is None in case of a new package. """
        if self.__package_id is not None:
            result['id'] = self.__package_id

        """Add a default organization if the owner org has not been assigned by the package creation logic."""
        if not 'owner_org' in self.__names_values:
            result['owner_org'] = organization_id

        for name in self.__names_values:
            result[name] = self.__names_values[name]

        return result