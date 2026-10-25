import logging

from rfcontrol.protocols import switch4

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch4.decode("01010101010101010101011001100110011001100110011002")
    assert decoded == {"unit": 31, "id": 0, "state": True}


def test_decode_2() -> None:
    decoded = switch4.decode("01100110011001100110010101010101010101010110010102")
    assert decoded == {"unit": 0, "id": 31, "state": False}


def test_decode_3() -> None:
    decoded = switch4.decode("01010110010101100110011001100110010101100110011002")
    assert decoded == {"unit": 20, "id": 2, "state": True}


def test_encode_1() -> None:
    encoded = switch4.encode(unit=31, id=0, state=True)
    assert encoded == "01010101010101010101011001100110011001100110011002"


def test_encode_2() -> None:
    encoded = switch4.encode(unit=0, id=31, state=False)
    assert encoded == "01100110011001100110010101010101010101010110010102"


def test_encode_3() -> None:
    encoded = switch4.encode(unit=20, id=2, state=True)
    assert encoded == "01010110010101100110011001100110010101100110011002"
