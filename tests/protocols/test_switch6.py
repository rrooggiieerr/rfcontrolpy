import logging

from rfcontrol.protocols import switch6

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch6.decode("10101010101010101010010101100110011001100110010102")
    assert decoded == {"id": 31, "unit": 1, "state": True}


def test_decode_2() -> None:
    decoded = switch6.decode("10101010101010100110011001010110011001100110010102")
    assert decoded == {"id": 15, "unit": 2, "state": True}


def test_encode_1() -> None:
    encoded = switch6.encode(id=31, unit=1, state=True)
    assert encoded == "10101010101010101010010101100110011001100110010102"


def test_encode_2() -> None:
    encoded = switch6.encode(id=15, unit=2, state=True)
    assert encoded == "10101010101010100110011001010110011001100110010102"
