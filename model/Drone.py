import typing


class Drone:
    """
    Represents a drone moving through a predefined route
    in the network.

    The drone keeps track of:
        - Its unique identifier.
        - The assigned route.
        - The current position in the route.
        - The current movement step.
    """
    def __init__(self, drone_id: int, route: list[str]) -> None:
        """
        Initialize a drone with an identifier and a route.

        Args:
            drone_id (int):
                Unique identifier of the drone.

            route (list[str]):
                Ordered list of hub names representing
                the drone's route.
        """
        self.__id = drone_id
        self.__route = route
        self.__current_step = 0
        self.__position = route[0] if route else None

    def getId(self) -> int:
        """
        Get the drone identifier.

        Returns:
            int:
                Unique drone ID.
        """
        return self.__id

    def getRoute(self) -> list[str]:
        """
        Get the complete route assigned to the drone.

        Returns:
            list[str]:
                List of hub names representing the route.
        """
        return self.__route

    def getPosition(self) -> typing.Any:
        """
        Get the drone's current position.

        Returns:
            typing.Any:
                Current hub name or None if no route exists.
        """
        return self.__position

    def getCurrentStep(self) -> int:
        """
        Get the current step index in the route.

        Returns:
            int:
                Current route step.
        """
        return self.__current_step

    def hasReachedGoal(self) -> bool:
        """
        Check whether the drone has reached the end
        of its route.

        Returns:
            bool:
                True if the drone reached the final hub,
                otherwise False.
        """
        return self.__current_step >= len(self.__route) - 1

    def move_next_step(self) -> typing.Any:
        """
        Move the drone to the next hub in its route.

        If the drone has already reached the destination,
        no movement occurs.

        Returns:
            typing.Any:
                True if the drone changed position,
                otherwise False.
        """
        if self.hasReachedGoal():
            return False

        posicion_anterior = self.__position
        self.__current_step += 1
        self.__position = self.__route[self.__current_step]
        return posicion_anterior != self.__position

    def __repr__(self) -> str:
        """
        Return a string representation of the drone.

        Returns:
            str:
                Readable representation including the drone ID
                and current position.
        """
        return f"Drone_{self.__id}(Pos: {self.__position})"

    def reset(self) -> None:
        """
        Reset the drone to its initial position.

        The drone returns to the first hub in its route
        and the current step counter is reset to zero.
        """
        self.__current_step = 0
        self.__position = self.__route[0] if self.__route else None
