import logging

from rfcontrol.protocols import weather15

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = weather15.decode(
        "0201010202010102010101010102010101010101020202010101020101020101010102010203"
    )
    assert decoded == {
        "id": 2448,
        "unit": 1,
        "temperature": 22.6,
        "humidity": 66,
        "lowBattery": False,
    }


def test_decode_2() -> None:
    decoded = weather15.decode(
        "0201010202010102010101010102010201010101020202010101020101020101010102010203"
    )
    assert decoded == {
        "id": 2448,
        "unit": 2,
        "temperature": 22.6,
        "humidity": 66,
        "lowBattery": False,
    }


def test_decode_3() -> None:
    decoded = weather15.decode(
        "0201010202010102010101010102020101010101020202010101020101020101010102010203"
    )
    assert decoded == {
        "id": 2448,
        "unit": 3,
        "temperature": 22.6,
        "humidity": 66,
        "lowBattery": False,
    }


def test_decode_4() -> None:
    decoded = weather15.decode(
        "0201010201010202010102020201010102020202020201020201020201010101020102010203"
    )
    assert decoded == {
        "id": 2355,
        "unit": 1,
        "temperature": -3.7,
        "humidity": 10,
        "lowBattery": True,
    }
