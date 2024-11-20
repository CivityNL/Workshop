from domain.package import Package


class PackageList:
    def __init__(self):
        super().__init__()
        self.__packages = {}
        self.__current = 0

    def add_package(self, package: Package) -> None:
        self.__packages[package.get_package_name()] = package

    def add_all_packages(self, package_list) -> None:
        for package in package_list:
            self.add_package(package)

    def get_package_by_index(self, index: int) -> Package:
        key: str = list(self.__packages)[index]
        return self.get_package_by_name(key)

    def get_package_by_name(self, package_name: str) -> Package:
        return self.__packages[package_name]

    def num_packages(self) -> int:
        return len(self.__packages)

    def get_keys(self):
        return self.__packages.keys()

    def __iter__(self):
        return self

    def __next__(self):
        if self.__current < self.num_packages():
            result: Package = self.get_package_by_index(self.__current)
            self.__current += 1
            return result

        self.__current = 0
        raise StopIteration

    def __str__(self):
        result: str = ''

        for i in range(0, self.num_packages()):
            package: Package = self.get_package_by_index(i)
            result += str(package)

        return result
