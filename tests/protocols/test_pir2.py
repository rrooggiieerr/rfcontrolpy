import logging

from rfcontrol.protocols import pir2

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = pir2.decode("01100110010110011001010110100101010101011010010102")
    assert decoded == {"id": 21, "unit": 21, "state": True}
