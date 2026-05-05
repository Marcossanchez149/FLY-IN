class Drone:
    def __init__(self, drone_id: int, route: list):
        self.__id = drone_id
        self.__route = route
        self.__current_step = 0
        self.__position = route[0] if route else None

    def getId(self) -> int:
        return self.__id

    def getRoute(self) -> list:
        return self.__route

    def getPosition(self) -> str:
        return self.__position

    def getCurrentStep(self) -> int:
        return self.__current_step

    def hasReachedGoal(self) -> bool:
        return self.__current_step >= len(self.__route) - 1

    def move_next_step(self) -> bool:
        if self.hasReachedGoal():
            return False

        posicion_anterior = self.__position
        self.__current_step += 1
        self.__position = self.__route[self.__current_step]
        return posicion_anterior != self.__position

    def __repr__(self) -> str:
        return f"Drone_{self.__id}(Pos: {self.__position})"

    def reset(self) -> None:
        self.__current_step = 0
        self.__position = self.__route[0] if self.__route else None
