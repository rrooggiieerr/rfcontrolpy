import logging

from rfcontrol.protocols import weather16

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = weather16.decode(
        "02020202010202010101020101010201010101010201010101010101010102020102010203"
    )
    assert decoded == {
        "id": 111,
        "unit": 1,
        "temperature": 26.0,
        "humidity": 36,
        "lowBattery": False,
    }


def test_decode_2() -> None:
    decoded = weather16.decode(
        "02020202010202010101020101010101010101010201010102010101010102020202020103"
    )
    assert decoded == {
        "id": 111,
        "unit": 1,
        "temperature": 25.6,
        "humidity": 37,
        "lowBattery": False,
    }
