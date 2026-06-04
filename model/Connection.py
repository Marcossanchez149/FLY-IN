class Connection:
    """
    Represents a bidirectional connection between two hubs
    in the drone network.

    A connection may optionally define a maximum link capacity
    that limits how many drones can use the connection
    simultaneously.
    """

    def __init__(self, hub1: str, hub2: str, max_link_capacity: int = 1):
        """
        Initialize a connection between two hubs.

        Args:
            hub1 (str):
                Name of the first hub.

            hub2 (str):
                Name of the second hub.

            max_link_capacity (int, optional):
                Maximum number of drones allowed on the connection
                at the same time.
        """
        self.__hub1 = hub1
        self.__hub2 = hub2
        self.__max_link_capacity = max_link_capacity

    def getHub1(self) -> str:
        """
        Get the name of the first hub.

        Returns:
            str:
                Name of the first hub.
        """
        return self.__hub1

    def getHub2(self) -> str:
        """
        Get the name of the second hub.

        Returns:
            str:
                Name of the second hub.
        """
        return self.__hub2

    def getMaxLink(self) -> int:
        """
        Get the maximum capacity of the connection.

        Returns:
            int:
                Maximum number of drones allowed simultaneously
                on this connection.
        """
        return self.__max_link_capacity

    def validate(self, h1: str, h2: str) -> bool:
        """
        Check whether the provided pair of hubs matches
        this connection.

        Since the connection is bidirectional, the order
        of the hubs does not matter.

        Args:
            h1 (str):
                Name of the first hub to compare.

            h2 (str):
                Name of the second hub to compare.

        Returns:
            bool:
                True if the hubs match this connection,
                otherwise False.
        """
        if (self.__hub1 == h1 and self.__hub2 == h2):
            return True
        elif (self.__hub1 == h2 and self.__hub2 == h1):
            return True
        else:
            return False
