from domain.enums.tipoAtaque import TipoAtaque
from domain.enums.cor import Cor
from domain.entities.cuboAtaque import CuboAtaque


class Cidade:
    def __init__(
        self,
        nome: str,
        pais: str,
        tipoAtaque: TipoAtaque,
        cidadesVizinhas: list["Cidade"],
        cubosAtaque: list[CuboAtaque],
        cor: Cor,
    ) -> None:
        self.__nome = nome
        self.__pais = pais
        self.__tipoAtaque = tipoAtaque
        self.__cidadesVizinhas = cidadesVizinhas
        self.__cubosAtaque = cubosAtaque
        self.__cor = cor

    # Getters
    def get_nome(self) -> str:
        return self.__nome

    def get_pais(self) -> str:
        return self.__pais

    def get_tipoAtaque(self) -> TipoAtaque:
        return self.__tipoAtaque

    def get_cidadesVizinhas(self) -> list["Cidade"]:
        return self.__cidadesVizinhas

    def get_cubosAtaque(self) -> list[CuboAtaque]:
        return self.__cubosAtaque

    def get_cor(self) -> Cor:
        return self.__cor

    # Setters
    def set_nome(self, nome: str) -> None:
        self.__nome = nome

    def set_pais(self, pais: str) -> None:
        self.__pais = pais

    def set_tipoAtaque(self, tipoAtaque: TipoAtaque) -> None:
        self.__tipoAtaque = tipoAtaque

    def set_cidadesVizinhas(self, vizinhas: list["Cidade"]) -> None:
        self.__cidadesVizinhas = vizinhas

    def set_cubosAtaque(self, cubosAtaque: CuboAtaque) -> None:
        self.__cubosAtaque.append(cubosAtaque)

    def set_cor(self, cor: Cor) -> None:
        self.__cor = cor

    # Verificação de surto
    def verificarSurto(self, cubo: CuboAtaque) -> bool:
        copia = self.__cubosAtaque.copy()
        copia.append(cubo)
        return len(copia) > 3

    def surto(self, qtd: CuboAtaque) -> None:
        for cidade in self.__cidadesVizinhas:
            if cidade.verificarSurto(qtd):
                cidade.set_cubosAtaque(qtd)
