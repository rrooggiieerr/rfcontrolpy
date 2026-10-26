import logging

from rfcontrol.protocols import switch28

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch28.decode("01010110010101100101011001100110011001010101101002")
    assert decoded == {"id": 11316396, "unit": 26213, "state": True, "all": False}


def test_decode_2() -> None:
    decoded = switch28.decode("01010110010101100101011001100110011001011010010102")
    assert decoded == {"id": 11316396, "unit": 26213, "state": False, "all": False}


def test_decode_3() -> None:
    decoded = switch28.decode("01010110010101100101011001100110011001010101010102")
    assert decoded == {"id": 11316396, "unit": 26213, "state": None, "all": True}


def test_encode_1() -> None:
    encoded = switch28.encode(id=8940720, unit=8164, state=True, all=True)
    assert encoded == "01000100001101100101100000011111111001000101010102"
