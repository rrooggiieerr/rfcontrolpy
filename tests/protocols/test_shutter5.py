import logging

from rfcontrol.protocols import shutter5

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = shutter5.decode("02210202022102022121022102212121020221212102020203")
    assert decoded == {"id": 281971, "command": "stop"}


def test_decode_2() -> None:
    decoded = shutter5.decode("02210202022102022121022102212121020221210202210203")
    assert decoded == {"id": 281971, "command": "up"}


def test_decode_3() -> None:
    decoded = shutter5.decode("02210202022102022121022102212121020221210221020203")
    assert decoded == {"id": 281971, "command": "down"}


def test_encode_1() -> None:
    encoded = shutter5.encode(id=281971, command="down")
    assert encoded == "02210202022102022121022102212121020221210221020203"
