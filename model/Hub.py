class Hub:
    """
    Represents a hub (or zone) in the drone network.

    A hub contains:
        - A unique name.
        - Coordinates on the map.
        - A display color.
        - A zone type.
        - A maximum drone capacity.
    """

    def __init__(self, name: str, posx: int, posy: int, color: str = "None",
                 zone: str = "Normal", max_drones: int = 1):
        """
        Initialize a hub with position and configuration data.

        Args:
            name (str):
                Unique hub name.

            posx (int):
                X coordinate of the hub.

            posy (int):
                Y coordinate of the hub.

            color (str, optional):
                Display color used for rendering the hub.

            zone (str, optional):
                Zone classification of the hub.

            max_drones (int, optional):
                Maximum number of drones allowed simultaneously
                at this hub.
        """
        self.__name = name
        self.__posx = posx
        self.__posy = posy
        self.__color = color
        self.__zone = zone
        self.__max_drones = max_drones

    def getName(self) -> str:
        """
        Get the hub name.

        Returns:
            str:
                Name of the hub.
        """
        return self.__name

    def getZone(self) -> str:
        """
        Get the zone type of the hub.

        Returns:
            str:
                Zone classification.
        """
        return self.__zone

    def getMaxDrones(self) -> int:
        """
        Get the maximum drone capacity of the hub.

        Returns:
            int:
                Maximum number of drones allowed at the hub.
        """
        return self.__max_drones

    def getPosx(self) -> int:
        """
        Get the X coordinate of the hub.

        Returns:
            int:
                X position.
        """
        return self.__posx

    def getPosy(self) -> int:
        """
        Get the Y coordinate of the hub.

        Returns:
            int:
                Y position.
        """
        return self.__posy

    def getColor(self) -> str:
        """
        Get the display color of the hub.

        Returns:
            str:
                Color name or value used for rendering.
        """
        return self.__color
