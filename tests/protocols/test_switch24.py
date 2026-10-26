import logging

from rfcontrol.protocols import switch24

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch24.decode("01101010010101011010101010011010100101010101011002")
    assert decoded == {"id": 17, "unit": 1, "state": True}


def test_encode_1() -> None:
    encoded = switch24.encode(id=17, unit=1, state=True)
    assert encoded == "01101010010101011010100110010110100101010101011002"
