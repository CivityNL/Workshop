class Resource:
    def __init__(self, resource_id: str, description: str, name: str, resource_format: str, url: str) -> None:
        super().__init__()
        self.__resource_id = resource_id
        self.__description = description
        self.__name = name
        self.__resource_format = resource_format
        self.__url = url

    def get_resource_id(self) -> str:
        return self.__resource_id

    def to_dict(self, package_id: str) -> dict:
        result = {
            'id': self.__resource_id,
            'description': self.__description,
            'name': self.__name,
            'package_id': package_id,
            'resource_format': self.__resource_format,
            'url': self.__url,
        }

        return result