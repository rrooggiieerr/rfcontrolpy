import logging

from rfcontrol.protocols import weather13

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = weather13.decode(
        "02010201010201010101010101010101020101020201020102020202010201010202010203"
    )
    assert decoded == {
        "id": 164,
        "unit": 1,
        "temperature": 15.4,
        "humidity": 77,
        "lowBattery": False,
    }


def test_decode_2() -> None:
    decoded = weather13.decode(
        "02010201010201010101010101010101010201020201020102020202010201020101010103"
    )
    assert decoded == {
        "id": 164,
        "unit": 1,
        "temperature": 9.0,
        "humidity": 80,
        "lowBattery": False,
    }


def test_decode_3() -> None:
    decoded = weather13.decode(
        "02020202010101020201020101010101020202010202010202020202010102020101010103"
    )
    assert decoded == {
        "id": 241,
        "unit": 3,
        "temperature": 23.70,
        "humidity": 48,
        "lowBattery": True,
    }
