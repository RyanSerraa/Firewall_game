import pytest
from domain.entities.controladorEpidemia import ControladorEpidemia


@pytest.fixture
def controlador():
    return ControladorEpidemia()


def test_nivel_inicial(controlador):
    assert controlador.get_nivel() == 2


def test_set_nivel(controlador):
    controlador.set_nivel(3)
    assert controlador.get_nivel() == 3


def test_increase_nivel_valido(controlador):
    controlador.increase_nivel(4)
    assert controlador.get_nivel() == 4


def test_increase_nivel_invalido(controlador):
    controlador.increase_nivel(6)
    assert controlador.get_nivel() == 2
