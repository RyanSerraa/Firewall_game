class ControladorSurto:
    def __init__(self) -> None:
        self.__nivel = 0

    def get_nivel(self) -> int:
        return self.__nivel

    def set_nivel(self) -> None:
        self.__nivel += 1

    def increase_nivel(self) -> None:
        if self.get_nivel() <= 7:
            self.set_nivel()
