import logging

from rfcontrol.protocols import alarm2

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = alarm2.decode("3002010101020102020201010101010102010101010201010104")
    assert decoded == {"id": 9142536, "state": True}


def test_encode_1() -> None:
    encoded = alarm2.encode(id=1960426, state=True)
    assert (
        encoded
        == "300101010202020102020202010201010202020201020102010430010101020202010202020201020101020202020102010201043001010102020201020202020102010102020202010201020104"
    )
