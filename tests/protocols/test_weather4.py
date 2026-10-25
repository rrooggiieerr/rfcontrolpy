import logging

from rfcontrol.protocols import weather4

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = weather4.decode(
        "11111111040303030203030302020302030203020302030302020202030302020202030303020202030202020305"
    )
    assert decoded == {
        "id": 238,
        "unit": 1,
        "temperature": 18.9,
        "humidity": 71,
        "lowBattery": False,
    }


def test_decode_2() -> None:
    decoded = weather4.decode(
        "11111111040203020303030302030302020203020302030302030202030202030202030303020202020202030305"
    )
    assert decoded == {
        "id": 94,
        "unit": 3,
        "temperature": 25.7,
        "humidity": 70,
        "lowBattery": False,
    }


def test_decode_3() -> None:
    decoded = weather4.decode(
        "11111111040302030203030303020302030202030202030303020202020202030302030203020302020202020305"
    )
    assert decoded == {
        "id": 175,
        "unit": 1,
        "temperature": 31.9,
        "humidity": 54,
        "lowBattery": False,
    }
