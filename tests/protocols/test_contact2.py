import logging

from rfcontrol.protocols import contact2

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = contact2.decode("10010110100101011010101010011001010101011001010102")
    assert decoded == {"id": 421983, "state": False}


def test_decode_2() -> None:
    decoded = contact2.decode("10010110100110011010010101101001010101011001010102")
    assert decoded == {"id": 414623, "state": False}
