import logging

from rfcontrol.protocols import switch15

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch15.decode("01101001011001100110010110011010101001011010101002")
    assert decoded == {"id": 414908, "unit": 1, "state": True, "all": False}


def test_decode_2() -> None:
    decoded = switch15.decode("01101001011001100110010110011010101001010110101002")
    assert decoded == {"id": 414908, "unit": 1, "state": False, "all": False}


def test_decode_3() -> None:
    decoded = switch15.decode("01101001011001100110010110011010101001011001101002")
    assert decoded == {"id": 414908, "unit": 2, "state": True, "all": False}


def test_decode_4() -> None:
    decoded = switch15.decode("01101001011001100110010110011010101001011001010102")
    assert decoded == {"id": 414908, "unit": 0, "state": False, "all": True}


def test_encode_1() -> None:
    encoded = switch15.encode(id=414908, unit=1, all=False, state=True)
    assert encoded == "01101001011001100110010110011010101001011010101002"
