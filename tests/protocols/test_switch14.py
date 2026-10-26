import logging

from rfcontrol.protocols import switch14

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch14.decode("01010101010101010101010101010101010101011010101002")
    assert decoded == {"id": 0, "unit": 1, "all": False, "state": True}


def test_decode_2() -> None:
    decoded = switch14.decode("01010101010101010101010101010101010101011010100102")
    assert decoded == {"id": 0, "unit": 1, "all": False, "state": False}


def test_decode_3() -> None:
    decoded = switch14.decode("01010101010101010101010101010101010101010110101002")
    assert decoded == {"id": 0, "unit": 2, "all": False, "state": True}


def test_decode_4() -> None:
    decoded = switch14.decode("01010101010101010101010101010101010101011010010102")
    assert decoded == {"id": 0, "unit": 1, "all": True, "state": False}


def test_encode_1() -> None:
    encoded = switch14.encode(id=0, unit=4, all=False, state=False)
    assert encoded == "01010101010101010101010101010101010101010101100102"
