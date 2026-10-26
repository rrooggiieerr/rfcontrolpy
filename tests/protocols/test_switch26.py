import logging

from rfcontrol.protocols import switch26

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch26.decode("01010110011001100110010101100110011001100110101002")
    assert decoded == {"channel": "A", "unit": "3", "state": True}


def test_decode_2() -> None:
    decoded = switch26.decode("01010110011001100110011001010110011001100110101002")
    assert decoded == {"channel": "A", "unit": "4", "state": True}


def test_decode_3() -> None:
    decoded = switch26.decode("01010110011001100110011001010110011001100110010102")
    assert decoded == {"channel": "A", "unit": "4", "state": False}


def test_encode_1() -> None:
    encoded = switch26.encode(channel="A", unit="3", state=True)
    assert encoded == "01010110011001100110010101100110011001100110101002"
