class Extent:
    def __init__(self, x_min: float, y_min: float, x_max: float, y_max: float, srs_code: int | None) -> None:
        self.__x_min: float = x_min
        self.__y_min: float = y_min
        self.__x_max: float = x_max
        self.__y_max: float = y_max
        self.__srs_code: int | None = srs_code

    def get_x_min(self) -> float:
        return self.__x_min

    def get_y_min(self) -> float:
        return self.__y_min

    def get_x_max(self) -> float:
        return self.__x_max

    def get_y_max(self) -> float:
        return self.__y_max

    def get_srs_code(self) -> int:
        return self.__srs_code

    def to_string(self) -> str:
        return f'[{self.__x_min}, {self.__y_min}, {self.__x_max}, {self.__y_max}]'
