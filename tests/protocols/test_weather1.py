import logging

from rfcontrol.protocols import weather1

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = weather1.decode(
        "01020102020201020101010101010102010101010202020102010101010102010101020103"
    )
    assert decoded == {
        "id": 208,
        "unit": 2,
        "temperature": 23.2,
        "humidity": 34,
        "lowBattery": True,
    }


def test_decode_2() -> None:
    decoded = weather1.decode(
        "01020102010201010101020202020101010101020101010101020101010102020202010203"
    )
    assert decoded == {
        "id": 67,
        "unit": 1,
        "temperature": 26.0,
        "humidity": 61,
        "lowBattery": False,
    }


def test_decode_3() -> None:
    decoded = weather1.decode(
        "01020102020201010102020102020101010101020101010101010101010102020202010103"
    )
    assert decoded == {
        "id": 198,
        "unit": 1,
        "temperature": 25.6,
        "humidity": 60,
        "lowBattery": False,
    }


def test_decode_4() -> None:
    decoded = weather1.decode(
        "01020102010102020102020102020201010101010202020201020101010201010101020203"
    )
    assert decoded == {
        "id": 54,
        "unit": 3,
        "temperature": 24.4,
        "humidity": 67,
        "lowBattery": False,
    }
