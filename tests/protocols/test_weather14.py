import logging

from rfcontrol.protocols import weather14

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = weather14.decode(
        "0102020102010202010101020202020202020202010101010102010201010202010102020203"
    )
    assert decoded == {"id": 78, "unit": 1, "temperature": 25.0, "lowBattery": True}


def test_decode_2() -> None:
    decoded = weather14.decode(
        "0102020102010202010101020202020201010101010102010102020101010202010102020203"
    )
    assert decoded == {"id": 78, "unit": 1, "temperature": -3.9, "lowBattery": True}


def test_decode_3() -> None:
    decoded = weather14.decode(
        "0201010201020102010101010102020101010102010101010202020202020101020201010103"
    )
    assert decoded == {
        "id": 175,
        "unit": 3,
        "temperature": -27.2,
        "lowBattery": False,
        "humidity": 51,
    }


def test_decode_4() -> None:
    decoded = weather14.decode(
        "0201010201020102010101010102010201010102010101010202010102020101020201010103"
    )
    assert decoded == {
        "id": 175,
        "unit": 3,
        "temperature": -26.9,
        "lowBattery": True,
        "humidity": 51,
    }
