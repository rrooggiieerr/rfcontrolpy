import logging

from rfcontrol.protocols import switch32

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch32.decode("01010110011001100101011001100110011001100110011002")
    assert decoded == {"id": 1, "unit": 1, "state": True}


def test_decode_2() -> None:
    decoded = switch32.decode("01010110011001100101011001100110011001100110010102")
    assert decoded == {"id": 1, "unit": 1, "state": False}


def test_decode_3() -> None:
    decoded = switch32.decode("01010110011001100110010101100110011001100110011002")
    assert decoded == {"id": 1, "unit": 2, "state": True}


def test_decode_4() -> None:
    decoded = switch32.decode("01010110011001100110010101100110011001100110010102")
    assert decoded == {"id": 1, "unit": 2, "state": False}


def test_decode_5() -> None:
    decoded = switch32.decode("01010110011001100110011001010110011001100110011002")
    assert decoded == {"id": 1, "unit": 3, "state": True}


def test_decode_6() -> None:
    decoded = switch32.decode("01010110011001100110011001010110011001100110010102")
    assert decoded == {"id": 1, "unit": 3, "state": False}


def test_decode_7() -> None:
    decoded = switch32.decode("01010110011001100110011001100101011001100110011002")
    assert decoded == {"id": 1, "unit": 4, "state": True}


def test_decode_8() -> None:
    decoded = switch32.decode("01010110011001100110011001100101011001100110010102")
    assert decoded == {"id": 1, "unit": 4, "state": False}


def test_decode_9() -> None:
    decoded = switch32.decode("01100101011001100101011001100110011001100110011002")
    assert decoded == {"id": 2, "unit": 1, "state": True}


def test_encode_1() -> None:
    encoded = switch32.encode(id=1, unit=1, state=True)
    assert encoded == "01010110011001100101011001100110011001100110011002"
