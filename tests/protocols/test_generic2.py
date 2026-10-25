import logging

from rfcontrol.protocols import generic2

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = generic2.decode(
        "011010101010101001011010101010101010101010010101101001101010100102"
    )
    assert decoded == {
        "id": 123,
        "type": 1,
        "value": 1023,
        "freq": 3,
        "battery": 99,
        "checksum": True,
    }


def test_decode_2() -> None:
    decoded = generic2.decode(
        "010110101010101001011010101010101010101010010101101001101010100102"
    )
    assert decoded == {
        "id": 123,
        "type": 1,
        "value": 1023,
        "freq": 3,
        "battery": 99,
        "checksum": False,
    }
