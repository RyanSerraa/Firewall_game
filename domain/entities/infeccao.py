from domain.entities.cidade import Cidade
from domain.entities.controladorSurto import ControladorSurto
from domain.entities.carta import Carta


class Infeccao(Carta):
    def __init__(self, cidade: Cidade) -> None:
        self.__cidade = cidade

    def get_cidade(self) -> Cidade:
        return self.__cidade

    def set_cidade(self, cidade: Cidade) -> None:
        self.__cidade = cidade

    def surto(self, qtd: int, controladorSurto: ControladorSurto) -> None:
        controladorSurto.set_nivel()
        self.__cidade.surto(qtd)

    def acao(self, parametro: tuple[int, ControladorSurto]) -> None:
        qtd, controladorSurto = parametro
        if not self.__cidade.verificarSurto(qtd):
            self.__cidade.set_cubosAtaque(qtd)
        else:
            self.surto(parametro, controladorSurto)
