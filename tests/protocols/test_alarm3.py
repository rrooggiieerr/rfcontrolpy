import logging

from rfcontrol.protocols import alarm3

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = alarm3.decode("100101010101100101011010010101101010101001011010000102")
    assert decoded == {"id": 9787738, "state": True}


def test_decode_2() -> None:
    decoded = alarm3.decode("011001100110011001100110011001100110011001100110000002")
    assert decoded == {"id": 6710886, "state": True}


def test_decode_3() -> None:
    decoded = alarm3.decode("011010101001010110010110100110101010101010100101111112")
    assert decoded == {"id": 6985110, "state": True}


def test_decode_4() -> None:
    decoded = alarm3.decode("011010101001001110010110100110101010101010100101111112")
    assert decoded == {"id": 6986089, "state": True}


def test_decode_5() -> None:
    decoded = alarm3.decode("101010100110100110100110010110100110101001011010000002")
    assert decoded == {"id": 11168166, "state": True}
