from domain.enums.tipoAtaque import TipoAtaque


class Cidade:
    def __init__(
        self,
        nome: str,
        pais: str,
        tipoAtaque: TipoAtaque,
        cidadesVizinhas: list["Cidade"],
        cubosAtaque: int,
    ) -> None:
        self.__nome = nome
        self.__pais = pais
        self.__tipoAtaque = tipoAtaque
        self.__cidadesVizinhas = cidadesVizinhas
        self.__cubosAtaque = cubosAtaque

    def get_nome(self) -> str:
        return self.__nome

    def set_nome(self, nome: str) -> None:
        self.__nome = nome

    def get_pais(self) -> str:
        return self.__pais

    def set_pais(self, pais: str) -> None:
        self.__pais = pais

    def get_tipoAtaque(self) -> TipoAtaque:
        return self.__tipoAtaque

    def set_tipoAtaque(self, tipoAtaque: TipoAtaque) -> None:
        self.__tipoAtaque = tipoAtaque

    def get_cubosAtaque(self) -> int:
        return self.__cubosAtaque

    def set_cubosAtaque(self, cubosAtaque: int) -> None:
        self.__cubosAtaque += cubosAtaque

    def verificarSurto(self, cubosAtaque: int) -> bool:
        if self.__cubosAtaque + cubosAtaque > 3:
            return True
        return False

    def get_cidadesVizinhas(self) -> list["Cidade"]:
        return self.__cidadesVizinhas

    def set_cidadesVizinhas(self, cidadesVizinhas: list["Cidade"]) -> None:
        self.__cidadesVizinhas = cidadesVizinhas

    def surto(self) -> None:
        for cidade in self.__cidadesVizinhas:
            if not cidade.verificarSurto(1):
                cidade.set_cubosAtaque(1)
