import logging

from rfcontrol.protocols import switch16

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch16.decode("01010110011001100101011001100110011001100110101002")
    assert decoded == {"id": "A", "unit": 1, "state": True}


def test_decode_2() -> None:
    decoded = switch16.decode("01010110011001100101011001100110011001100110010102")
    assert decoded == {"id": "A", "unit": 1, "state": False}


def test_decode_3() -> None:
    decoded = switch16.decode("01010110011001100110010101100110011001100110101002")
    assert decoded == {"id": "A", "unit": 2, "state": True}


def test_decode_4() -> None:
    decoded = switch16.decode("01010110011001100110010101100110011001100110010102")
    assert decoded == {"id": "A", "unit": 2, "state": False}


def test_decode_5() -> None:
    decoded = switch16.decode("01010110011001100110011001100110011001100110101002")
    assert decoded == {"id": "A", "unit": 3, "state": True}


def test_decode_6() -> None:
    decoded = switch16.decode("01010110011001100110011001010110011001100110010102")
    assert decoded == {"id": "A", "unit": 3, "state": False}


def test_decode_7() -> None:
    decoded = switch16.decode("01100101011001100101011001100110011001100110101002")
    assert decoded == {"id": "B", "unit": 1, "state": True}


def test_decode_8() -> None:
    decoded = switch16.decode("01100101011001100101011001100110011001100110010102")
    assert decoded == {"id": "B", "unit": 1, "state": False}


def test_decode_9() -> None:
    decoded = switch16.decode("01100101011001100110011001100110011001100110101002")
    assert decoded == {"id": "B", "unit": 3, "state": True}


def test_decode_10() -> None:
    decoded = switch16.decode("01100101011001100110011001010110011001100110010102")
    assert decoded == {"id": "B", "unit": 3, "state": False}


def test_encode_1() -> None:
    encoded = switch16.encode(id="A", unit=2, state=False)
    assert encoded == "01010110011001100110010101100110011001100110010102"
