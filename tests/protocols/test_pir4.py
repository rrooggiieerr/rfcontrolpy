import logging

from rfcontrol.protocols import pir4

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = pir4.decode("110100110101001101010011001010101012")
    assert decoded == {"id": 54099, "unit": 21290, "state": True}
