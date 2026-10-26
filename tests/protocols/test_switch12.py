import logging

from rfcontrol.protocols import switch12

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch12.decode("1202021212021212121212121212021212121212121212121203")
    assert decoded == {"id": 9983, "unit": 1, "state": True}


def test_decode_2() -> None:
    decoded = switch12.decode("1202021212021212121212121212121212121202121202021203")
    assert decoded == {"id": 9983, "unit": 1, "state": False}


def test_decode_3() -> None:
    decoded = switch12.decode("1202021212021212121212121212121212021212121202120213")
    assert decoded == {"id": 9983, "unit": 2, "state": True}


def test_decode_4() -> None:
    decoded = switch12.decode("1202021212021212121212121212121202121212121202120203")
    assert decoded == {"id": 9983, "unit": 3, "state": True}


def test_encode_1() -> None:
    encoded = switch12.encode(id=9983, unit=1, state=True)
    assert encoded == "1202021212021212121212121212021212121212121212121203"
