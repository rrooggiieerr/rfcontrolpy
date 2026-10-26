import logging

from rfcontrol.protocols import shutter4

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = shutter4.decode(
        "3201010110010101100101100101010101100101101010100101011001010101010101011001010113"
    )
    assert decoded == {"id": 17959394, "unit": 0, "all": True, "command": "up"}


def test_decode_2() -> None:
    decoded = shutter4.decode(
        "3201010110010101100101100101010101100101101010100101011001010110100110011001100113"
    )
    assert decoded == {"id": 17959394, "unit": 3, "all": False, "command": "stop"}


def test_decode_3() -> None:
    decoded = shutter4.decode(
        "3201010110010101100101100101010101100101101010100101011001011001100101101010100103"
    )
    assert decoded == {"id": 17959394, "unit": 5, "all": False, "command": "down"}


def test_decode_4() -> None:
    decoded = shutter4.decode(
        "3201011001010101010110010101010101010110100101011001100101100101100101011001010113"
    )
    assert decoded == {"id": 33817364, "unit": 9, "all": False, "command": "up"}


def test_encode_1() -> None:
    encoded = shutter4.encode(id=17959394, unit=0, all=True, command="up")
    assert (
        encoded
        == "3201010110010101100101100101010101100101101010100101011001010101010101011001010113"
    )
