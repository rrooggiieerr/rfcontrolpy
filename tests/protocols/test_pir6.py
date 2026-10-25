import logging

from rfcontrol.protocols import pir6

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = pir6.decode("01011010010101011010100110010101101001010101101002")
    assert decoded == {"id": 6410630, "state": True}


def test_decode_2() -> None:
    decoded = pir6.decode("01011010010101011010100110010101101001010110010102")
    assert decoded == {"id": 6410632, "state": True}


def test_decode_3() -> None:
    decoded = pir6.decode("01011010010101011010100110010101101001011001010102")
    assert decoded == {"id": 6410640, "state": True}
