import logging

from rfcontrol.protocols import shutter3

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = shutter3.decode(
        "3210010110010101010110011010011010010110100101011001011001100101101010010110100104"
    )
    assert decoded == {"id": 151368466, "unit": 9, "command": "program"}


def test_decode_2() -> None:
    decoded = shutter3.decode(
        "3210011010100110010101101001010110011010011001100110010101010101101010010110100104"
    )
    assert decoded == {"id": 195237544, "unit": 1, "command": "program"}


def test_encode_1() -> None:
    encoded = shutter3.encode(id=151368466, unit=9, command="program")
    assert (
        encoded
        == "3210010110010101010110011010011010010110100101011001011001100101101010010110100104"
    )
