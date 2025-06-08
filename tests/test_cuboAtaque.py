import pytest
from domain.entities.cuboAtaque import CuboAtaque
from domain.enums.tipoAtaque import TipoAtaque
from domain.enums.cor import Cor


class TestCuboAtaque:
    def test_init(self):
        """Testa a inicialização correta dos atributos"""
        cubo = CuboAtaque(ataque=TipoAtaque.RANSOMWARE, cor=Cor.VERMELHO)

        assert cubo.get_ataque() == TipoAtaque.RANSOMWARE
        assert cubo.get_cor() == Cor.VERMELHO

    def test_getters(self):
        """Testa se os getters retornam os valores corretos"""
        cubo = CuboAtaque(ataque=TipoAtaque.PHISHING, cor=Cor.AZUL)

        assert isinstance(cubo.get_ataque(), TipoAtaque)
        assert cubo.get_ataque().value == "Phishing"

        assert isinstance(cubo.get_cor(), Cor)
        assert cubo.get_cor().value == "#1100FF"

    def test_setters(self):
        """Testa se os setters alteram os valores corretamente"""
        cubo = CuboAtaque(ataque=TipoAtaque.DDOS, cor=Cor.AMARELO)

        # Testa set_ataque
        cubo.set_ataque(TipoAtaque.SPYWARE)
        assert cubo.get_ataque() == TipoAtaque.SPYWARE

        # Testa set_cor
        cubo.set_cor(Cor.PRETO)
        assert cubo.get_cor() == Cor.PRETO

    @pytest.mark.parametrize(
        "ataque,cor",
        [
            (TipoAtaque.RANSOMWARE, Cor.VERMELHO),
            (TipoAtaque.PHISHING, Cor.AZUL),
            (TipoAtaque.DDOS, Cor.AMARELO),
            (TipoAtaque.SPYWARE, Cor.PRETO),
        ],
    )
    def test_combinations(self, ataque, cor):
        """Testa várias combinações de ataque e cor"""
        cubo = CuboAtaque(ataque=ataque, cor=cor)

        assert cubo.get_ataque() == ataque
        assert cubo.get_cor() == cor

    def test_invalid_types(self):
        """Testa se tipos inválidos são rejeitados"""
        with pytest.raises(TypeError):
            CuboAtaque(ataque="ataque", cor="cor")
