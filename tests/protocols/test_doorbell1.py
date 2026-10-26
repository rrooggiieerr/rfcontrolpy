import logging

from rfcontrol.protocols import doorbell1

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = doorbell1.decode("01101010011001100110011010101010101010101010101002")
    assert decoded == {"id": 1361, "unit": 0, "state": True}


def test_encode_1() -> None:
    encoded = doorbell1.encode(id=1361, unit=0, state=True)
    assert encoded == "01101010011001100110011010101010101010101010101002"
