import logging

from rfcontrol.protocols import weather12

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = weather12.decode(
        "0102020201010102020101010101010101020202020102020201020102010202020102020103"
    )
    assert decoded == {
        "id": 113,
        "unit": 1,
        "temperature": 12.3,
        "humidity": 85,
        "lowBattery": True,
    }


def test_decode_2() -> None:
    decoded = weather12.decode(
        "0201010202010202010101010101010101020201010202010202010202020102020201010203"
    )
    assert decoded == {
        "id": 155,
        "unit": 1,
        "temperature": 10.2,
        "humidity": 110,
        "lowBattery": False,
    }


def test_decode_3() -> None:
    decoded = weather12.decode(
        "0201010202010202010101010101010101020202010202020201020101010102010202010103"
    )
    assert decoded == {
        "id": 155,
        "unit": 1,
        "temperature": 11.9,
        "humidity": 80,
        "lowBattery": False,
    }
