from domain.entities.cidade import Cidade
from domain.entities.cuboAtaque import CuboAtaque
from domain.enums.tipoAtaque import TipoAtaque
from domain.enums.cor import Cor


def test_getters_and_setters():
    cuboAtaque = CuboAtaque(TipoAtaque.RANSOMWARE, Cor.VERMELHO)
    cidade = Cidade(
        nome="Cidade1",
        pais="Pais1",
        tipoAtaque=TipoAtaque.RANSOMWARE,
        cidadesVizinhas=[],
        cubosAtaque=[cuboAtaque],
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
    assert cidade.get_cubosAtaque() == [cuboAtaque]
    novo_cubo = CuboAtaque(TipoAtaque.SPYWARE, Cor.AZUL)
    cidade.set_cubosAtaque(novo_cubo)
    assert cidade.get_cubosAtaque() == [cuboAtaque, novo_cubo]
    novo_cubo2 = CuboAtaque(TipoAtaque.DDOS, Cor.AMARELO)
    cidade.set_cubosAtaque(novo_cubo2)
    assert cidade.get_cubosAtaque() == [cuboAtaque, novo_cubo, novo_cubo2]


def test_verificarSurto():
    cubosAtaque = [
        CuboAtaque(TipoAtaque.RANSOMWARE, Cor.VERMELHO),
        CuboAtaque(TipoAtaque.PHISHING, Cor.VERMELHO),
    ]
    c = Cidade("Cidade", "Pais", TipoAtaque.DDOS, [], cubosAtaque, cor=Cor.VERMELHO)
    # 2 + 1 <= 3 => False (não gera surto)
    assert c.verificarSurto(cubosAtaque[0]) is False
    c.set_cubosAtaque(cubosAtaque[1])
    # 2 + 2 > 3 => True (gera surto)
    assert c.verificarSurto(cubosAtaque[0]) is True


def test_surtos_em_cidades_vizinhas():
    cubosAtaque = [
        CuboAtaque(TipoAtaque.RANSOMWARE, Cor.VERMELHO),
        CuboAtaque(TipoAtaque.PHISHING, Cor.VERMELHO),
        CuboAtaque(TipoAtaque.DDOS, Cor.VERMELHO),
    ]
    cidade1 = Cidade(
        "Cidade1",
        "Pais",
        TipoAtaque.SPYWARE,
        [],
        [cubosAtaque[0], cubosAtaque[1]],
        cor=Cor.VERMELHO,
    )
    cidade2 = Cidade(
        "Cidade2", "Pais", TipoAtaque.SPYWARE, [], cubosAtaque, cor=Cor.VERMELHO
    )
    cidade3 = Cidade(
        "Cidade3", "Pais", TipoAtaque.SPYWARE, [], [cubosAtaque[0]], cor=Cor.VERMELHO
    )

    cidade_central = Cidade(
        "Central",
        "Pais",
        TipoAtaque.SPYWARE,
        [cidade1, cidade2, cidade3],
        cubosAtaque[1],
        cor=Cor.VERMELHO,
    )

    cidade_central.surto(cubosAtaque[2])

    # cidade1 e cidade3 devem ter incrementado cubosAtaque
    assert len(cidade1.get_cubosAtaque()) == 3  # 2 + 1
    assert len(cidade2.get_cubosAtaque()) == 3  # não incrementou pois geraria surto
    assert len(cidade3.get_cubosAtaque()) == 2  # 1 + 1
