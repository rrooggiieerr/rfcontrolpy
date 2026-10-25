import logging

from rfcontrol.protocols import switch7

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch7.decode("01010101010101100110011001100110011001100110011002")
    assert decoded == {"id": 0, "unit": 3, "state": True}


def test_decode_2() -> None:
    decoded = switch7.decode("01010101010101100101010101010110011001100110011002")
    assert decoded == {"id": 7, "unit": 3, "state": True}


def test_decode_3() -> None:
    decoded = switch7.decode("10100101011001100101010101010110011001100110011002")
    assert decoded == {"id": 7, "unit": 1, "state": False}


def test_encode_1() -> None:
    encoded = switch7.encode(id=0, unit=3, state=True)
    assert encoded == "01010101010101100110011001100110011001100110011002"


def test_encode_2() -> None:
    encoded = switch7.encode(id=7, unit=3, state=True)
    assert encoded == "01010101010101100101010101010110011001100110011002"


def test_encode_3() -> None:
    encoded = switch7.encode(id=7, unit=1, state=False)
    assert encoded == "10100101011001100101010101010110011001100110011002"
