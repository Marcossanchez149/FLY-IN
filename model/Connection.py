class Connection:

    def __init__(self, hub1: str, hub2: str, max_link_capacity: int = 1):
        self.__hub1 = hub1
        self.__hub2 = hub2
        self.__max_link_capacity = max_link_capacity

    def getHub1(self) -> str:
        return self.__hub1

    def getHub2(self) -> str:
        return self.__hub2

    def getMaxLink(self) -> int:
        return self.__max_link_capacity

    def validate(self, h1: str, h2: str) -> bool:
        if (self.__hub1 == h1 and self.__hub2 == h2):
            return True
        elif (self.__hub1 == h2 and self.__hub2 == h1):
            return True
        else:
            return False
