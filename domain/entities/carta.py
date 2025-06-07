from abc import ABC, abstractmethod
from typing import Any


class Carta(ABC):
    def __init__(self, nome: str) -> None:
        self.__nome = nome

    def get_nome(self) -> str:
        return self.__nome

    def set_nome(self, nome: str) -> None:
        self.__nome = nome

    @abstractmethod
    def acao(self, parametro: Any) -> None:
        pass
