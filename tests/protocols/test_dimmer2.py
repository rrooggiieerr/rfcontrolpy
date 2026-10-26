import logging

from rfcontrol.protocols import dimmer2

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = dimmer2.decode(
        "010101010102010201010101020102020102010101010101010201010202010201010101020101020101010201020101010102010102010101020102010101010201010201010103"
    )
    assert decoded == {"id": 16711422, "unit": 15, "state": True, "dimlevel": 0}


def test_decode_unknown_nibble() -> None:
    # The unit nibble is 0000000, which isn't one of the 16 nibble codes.
    decoded = dimmer2.decode(
        "010101010102010201010101020102020202020202020101010201010202010201010101020101020101010201020101010102010102010101020102010101010201010201010103"
    )
    assert decoded is None


def test_encode_1() -> None:
    encoded = dimmer2.encode(id=16711422, unit=15, dimlevel=5)
    assert (
        encoded
        == "010102010101020101010201010201020102010101010101010201010202010201010101020101020101010201020101010102010102010101020102010101010201010201010103"
    )
