import pytest
from domain.entities.controladorSurto import ControladorSurto


@pytest.fixture
def controlador():
    return ControladorSurto()


def test_nivel_inicial(controlador):
    assert controlador.get_nivel() == 0


def test_set_nivel_incrementa(controlador):
    controlador.set_nivel()
    assert controlador.get_nivel() == 1
    controlador.set_nivel()
    assert controlador.get_nivel() == 2


def test_increase_nivel_abaixo_limite(controlador):
    for _ in range(5):
        controlador.increase_nivel()
    assert controlador.get_nivel() == 5


def test_increase_nivel_no_limite(controlador):
    for _ in range(8):
        controlador.increase_nivel()
    assert controlador.get_nivel() == 8
