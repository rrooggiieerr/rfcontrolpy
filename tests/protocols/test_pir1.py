import logging

from rfcontrol.protocols import pir1

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = pir1.decode("01100101011001100110011001100110011001010110011002")
    assert decoded == {"id": 1, "unit": 8, "state": True}


def test_decode_2() -> None:
    decoded = pir1.decode("01100110011001100110010101100110011001010110011002")
    assert decoded == {"id": 17, "unit": 0, "state": True}


def test_decode_3() -> None:
    decoded = pir1.decode("01100110011001010110011001100110010101100110011002")
    assert decoded == {"id": 2, "unit": 2, "state": True}
