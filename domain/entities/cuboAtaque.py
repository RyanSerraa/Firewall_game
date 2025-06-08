from domain.enums.cor import Cor
from domain.enums.tipoAtaque import TipoAtaque


class CuboAtaque:
    def __init__(self, ataque: TipoAtaque, cor: Cor) -> None:
        if not isinstance(ataque, TipoAtaque):
            raise TypeError(f"Esperado TipoAtaque, recebido {type(ataque)}")
        if not isinstance(cor, Cor):
            raise TypeError(f"Esperado Cor, recebido {type(cor)}")

        self.__ataque = ataque
        self.__cor = cor

    def get_ataque(self) -> TipoAtaque:
        return self.__ataque

    def get_cor(self) -> Cor:
        return self.__cor

    def set_ataque(self, ataque: TipoAtaque) -> None:
        self.__ataque = ataque

    def set_cor(self, cor: Cor) -> None:
        self.__cor = cor
