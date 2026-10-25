import logging

from rfcontrol.protocols import switch8

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch8.decode("01010101010101010110011001100110101001011010010102")
    assert decoded == {"id": 30, "unit": "B1", "state": False}


def test_decode_2() -> None:
    decoded = switch8.decode("01010101010101010110011001101010010101010101101002")
    assert decoded == {"id": 30, "unit": "C3", "state": True}


def test_decode_3() -> None:
    decoded = switch8.decode("01010101010101010101011001101010010101010101101002")
    assert decoded == {"id": 31, "unit": "C3", "state": True}


def test_decode_4() -> None:
    decoded = switch8.decode("01100110011001100101011001101010011001010101101002")
    assert decoded == {"id": 1, "unit": "C1", "state": True}


def test_decode_5() -> None:
    decoded = switch8.decode("01100110011001100101011001101010010101100101101002")
    assert decoded == {"id": 1, "unit": "C2", "state": True}


def test_encode_1() -> None:
    encoded = switch8.encode(id=30, unit="B1", state=False)
    assert encoded == "01010101010101010110011001100110101001011010010102"


def test_encode_2() -> None:
    encoded = switch8.encode(id=30, unit="C3", state=True)
    assert encoded == "01010101010101010110011001101010010101010101101002"


def test_encode_3() -> None:
    encoded = switch8.encode(id=31, unit="C3", state=True)
    assert encoded == "01010101010101010101011001101010010101010101101002"


def test_encode_4() -> None:
    encoded = switch8.encode(id=1, unit="C1", state=True)
    assert encoded == "01100110011001100101011001101010011001010101101002"


def test_encode_5() -> None:
    encoded = switch8.encode(id=1, unit="C2", state=True)
    assert encoded == "01100110011001100101011001101010010101100101101002"
