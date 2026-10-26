import logging

from rfcontrol.protocols import doorbell2

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = doorbell2.decode("101010011001100110010101011001011010100110010102")
    assert decoded == {"unit": 343, "id": 1419, "state": True}


def test_encode_1() -> None:
    encoded = doorbell2.encode(id=1419, unit=343)
    assert encoded == "101010011001100110010101011001011010100110010102"
