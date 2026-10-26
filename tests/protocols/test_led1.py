import logging

from rfcontrol.protocols import led1

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = led1.decode("01100110100101011001100110101001010110010101011002")
    assert decoded == {"id": 22702, "command": "on/off"}


def test_decode_2() -> None:
    decoded = led1.decode("01011010010101100110011010101001010110010101011002")
    assert decoded == {"id": 12638, "command": "on/off"}


def test_decode_3() -> None:
    decoded = led1.decode("01100110100101011001100110101001010110010110010102")
    assert decoded == {"id": 22702, "command": "up"}


def test_decode_4() -> None:
    decoded = led1.decode("01100110100101011001100110101001010110010101100102")
    assert decoded == {"id": 22702, "command": "down"}


def test_encode_1() -> None:
    encoded = led1.encode(id=23241, command="on/off")
    assert encoded == "01100110100110011010010110010110010110010101011002"
