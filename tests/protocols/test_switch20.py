import logging

from rfcontrol.protocols import switch20

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch20.decode("01100110010101100110011001100110011001100110011002")
    assert decoded == {"unit": 0, "state": True}


def test_encode_1() -> None:
    encoded = switch20.encode(unit=10, state=False)
    assert encoded == "01100110010101100101011001010101011001100101011002"
