from .Hub import Hub
from .Connection import Connection


class Map:
    """
    Represents the complete drone network map.

    The map contains:
        - The total number of drones.
        - The starting hub.
        - The destination hub.
        - All intermediate hubs.
        - All valid connections between hubs.
    """
    def __init__(self, nbDrones: int, startHub: Hub, endHub: Hub,
                 hubs: list[Hub], conecctions: list[Connection]) -> None:
        """
        Initialize the network map.

        Args:
            nbDrones (int):
                Total number of drones in the simulation.

            startHub (Hub):
                Starting hub for all drones.

            endHub (Hub):
                Destination hub for all drones.

            hubs (list[Hub]):
                List of hubs contained in the network.

            conecctions (list[Connection]):
                List of valid connections between hubs.
        """
        self.__nbDrones = nbDrones
        self.__startHub = startHub
        self.__endHub = endHub
        self.__hubs = hubs
        self.__conecctions = conecctions

    def getStartHub(self) -> Hub:
        """
        Get the starting hub of the network.

        Returns:
            Hub:
                The start hub.
        """
        return self.__startHub

    def getEndHub(self) -> Hub:
        """
        Get the destination hub of the network.

        Returns:
            Hub:
                The end hub.
        """
        return self.__endHub

    def getHubs(self) -> list[Hub]:
        """
        Get all hubs in the network.

        Returns:
            list[Hub]:
                List of hubs.
        """
        return self.__hubs

    def getConnections(self) -> list[Connection]:
        """
        Get all network connections.

        Returns:
            list[Connection]:
                List of connections.
        """
        return self.__conecctions

    def getNbDrones(self) -> int:
        """
        Get the total number of drones.

        Returns:
            int:
                Number of drones in the simulation.
        """
        return self.__nbDrones

    def validateConnection(self, origin: str, destiny: str) -> bool:
        """
        Check whether a valid connection exists between two hubs.

        Args:
            origin (str):
                Name of the origin hub.

            destiny (str):
                Name of the destination hub.

        Returns:
            bool:
                True if a connection exists between the hubs,
                otherwise False.
        """
        for con in self.__conecctions:
            if (con.validate(origin, destiny)):
                return True
        return False
