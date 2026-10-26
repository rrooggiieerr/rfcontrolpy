import logging

from rfcontrol.protocols import weather21

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = weather21.decode(
        "1222222220122012121212201220121220121212121212121212121220122020121221212112121221121213"
    )
    assert decoded == {
        "crcOk": True,
        "id": 161,
        "humidity": 72,
        "lowBattery": False,
        "unit": 1,
        "temperature": 17.9,
    }


def test_decode_2() -> None:
    decoded = weather21.decode(
        "1222222220122012121212201220121212201220121212121212121220122020122020201212121212121213"
    )
    assert decoded == {
        "crcOk": True,
        "id": 161,
        "humidity": 69,
        "lowBattery": False,
        "unit": 1,
        "temperature": 18.3,
    }


def test_decode_3() -> None:
    decoded = weather21.decode(
        "1222222220122012121212201220121212122020121212121212121220201212121220122112201221122123"
    )
    assert decoded == {
        "crcOk": False,
        "id": 161,
        "humidity": 67,
        "lowBattery": False,
        "unit": 1,
        "temperature": 19.4,
    }


def test_decode_4() -> None:
    decoded = weather21.decode(
        "1222222220122012121212201220121212122121121212121212121221211212121221122112211221122123"
    )
    assert decoded == {
        "crcOk": False,
        "id": 161,
        "humidity": 67,
        "lowBattery": False,
        "unit": 1,
        "temperature": 19.4,
    }
