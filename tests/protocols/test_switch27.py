import logging

from rfcontrol.protocols import switch27

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch27.decode("01100110011001100101011001100110011001100110101002")
    assert decoded == {"channel": "A", "unit": "1", "state": True}


def test_decode_2() -> None:
    decoded = switch27.decode("01100110010101100101011001100110011001100110101002")
    assert decoded == {"channel": "C", "unit": "1", "state": True}


def test_decode_3() -> None:
    decoded = switch27.decode("01100110011001010101011001100110011001100110101002")
    assert decoded == {"channel": "D", "unit": "1", "state": True}


def test_encode_1() -> None:
    encoded = switch27.encode(channel="C", unit="2", state=False)
    assert encoded == "01100110010101100110010101100110011001100110010102"
