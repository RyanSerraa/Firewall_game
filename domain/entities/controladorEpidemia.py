class ControladorEpidemia:
    def __init__(self) -> None:
        self.__nivel = 2

    def get_nivel(self) -> str:
        return self.__nivel

    def set_nivel(self, nivel: int) -> None:
        self.__nivel = nivel

    def increase_nivel(self, nivel: int) -> None:
        if nivel in [2, 3, 4]:
            self.set_nivel(nivel)
