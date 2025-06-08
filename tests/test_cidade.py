from domain.entities.cidade import Cidade
from domain.enums.tipoAtaque import TipoAtaque
from domain.enums.cor import Cor


def test_getters_and_setters():
    cidade = Cidade(
        nome="Cidade1",
        pais="Pais1",
        tipoAtaque=TipoAtaque.RANSOMWARE,
        cidadesVizinhas=[],
        cubosAtaque=0,
        cor=Cor.VERMELHO,
    )

    # Teste get_nome e set_nome
    assert cidade.get_nome() == "Cidade1"
    cidade.set_nome("Cidade2")
    assert cidade.get_nome() == "Cidade2"

    # Teste get_pais e set_pais
    assert cidade.get_pais() == "Pais1"
    cidade.set_pais("Pais2")
    assert cidade.get_pais() == "Pais2"

    # Teste get_tipoAtaque e set_tipoAtaque
    assert cidade.get_tipoAtaque() == TipoAtaque.RANSOMWARE
    cidade.set_tipoAtaque(TipoAtaque.PHISHING)
    assert cidade.get_tipoAtaque() == TipoAtaque.PHISHING

    # Teste get_cubosAtaque e set_cubosAtaque (incremento)
    assert cidade.get_cubosAtaque() == 0
    cidade.set_cubosAtaque(2)
    assert cidade.get_cubosAtaque() == 2
    cidade.set_cubosAtaque(1)
    assert cidade.get_cubosAtaque() == 3


def test_verificarSurto():
    c = Cidade("Cidade", "Pais", TipoAtaque.DDOS, [], 2, cor=Cor.VERMELHO)
    # 2 + 1 <= 3 => False (não gera surto)
    assert c.verificarSurto(1) is False
    # 2 + 2 > 3 => True (gera surto)
    assert c.verificarSurto(2) is True


def test_surtos_em_cidades_vizinhas():
    cidade1 = Cidade("Cidade1", "Pais", TipoAtaque.SPYWARE, [], 2, cor=Cor.VERMELHO)
    cidade2 = Cidade("Cidade2", "Pais", TipoAtaque.SPYWARE, [], 3, cor=Cor.VERMELHO)
    cidade3 = Cidade("Cidade3", "Pais", TipoAtaque.SPYWARE, [], 1, cor=Cor.VERMELHO)

    cidade_central = Cidade(
        "Central",
        "Pais",
        TipoAtaque.SPYWARE,
        [cidade1, cidade2, cidade3],
        0,
        cor=Cor.VERMELHO,
    )

    cidade_central.surto()

    # cidade1 e cidade3 devem ter incrementado cubosAtaque
    assert cidade1.get_cubosAtaque() == 3  # 2 + 1
    assert cidade2.get_cubosAtaque() == 3  # não incrementou pois geraria surto
    assert cidade3.get_cubosAtaque() == 2  # 1 + 1
