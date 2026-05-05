from .Hub import Hub
from .Connection import Connection


class Map:
    def __init__(self, nbDrones: int, startHub: Hub, endHub: Hub,
                 hubs: list[Hub], conecctions: list[Connection]) -> None:
        self.__nbDrones = nbDrones
        self.__startHub = startHub
        self.__endHub = endHub
        self.__hubs = hubs
        self.__conecctions = conecctions

    def getStartHub(self) -> Hub:
        return self.__startHub

    def getEndHub(self) -> Hub:
        return self.__endHub

    def getHubs(self) -> list[Hub]:
        return self.__hubs

    def getConnections(self) -> Connection:
        return self.__conecctions

    def getNbDrones(self) -> int:
        return self.__nbDrones

    def validateConnection(self, origin: str, destiny: str) -> bool:
        for con in self.__conecctions:
            if (con.validate(origin, destiny)):
                return True
        return False
