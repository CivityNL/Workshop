class Package:
    def __init__(self, package_id: str) -> None:
        super().__init__()
        self.__package_id = package_id

    def get_package_id(self) -> str:
        return self.__package_id