class Hub:

    def __init__(self, name: str, posx: int, posy: int, color: str = "White",
                 zone: str = "Normal", max_drones: int = 1):
        self.__name = name
        self.__posx = posx
        self.__posy = posy
        self.__color = color
        self.__zone = zone
        self.__max_drones = max_drones

    def getName(self) -> str:
        return self.__name

    def getZone(self) -> str:
        return self.__zone

    def getMaxDrones(self) -> int:
        return self.__max_drones

    def getPosx(self) -> int:
        return self.__posx

    def getPosy(self) -> int:
        return self.__posy

    def getColor(self) -> str:
        return self.__color
