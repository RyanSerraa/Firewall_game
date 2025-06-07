class ControladorSurto:
    def __init__(self) -> None:
        self.__nivel = 0

    def get_nivel(self) -> str:
        return self.__nivel

    def set_nivel(self) -> None:
        self.__nivel += 1
