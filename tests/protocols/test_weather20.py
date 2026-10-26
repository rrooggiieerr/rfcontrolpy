import logging

from rfcontrol.protocols import weather20

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = weather20.decode(
        "0302020302020202030202020302020202020202030302020202030202020202020202020104"
    )
    assert decoded == {"id": 2312, "unit": 1, "temperature": 19.4, "lowBattery": True}


def test_decode_2() -> None:
    decoded = weather20.decode(
        "0302020302020202030202020302020202020202030203030302030202020202020202020104"
    )
    assert decoded == {"id": 2312, "unit": 1, "temperature": 18.6, "lowBattery": True}


def test_decode_3() -> None:
    decoded = weather20.decode(
        "0302020302020202030202020302020202020202030203030302030302020202020202020104"
    )
    assert decoded == {"id": 2312, "unit": 1, "temperature": 18.7, "lowBattery": True}


def test_decode_4() -> None:
    decoded = weather20.decode(
        "0302020302020202030302030302020302020202030302020203030202020202020202020104"
    )
    assert decoded == {"id": 2317, "unit": 2, "temperature": 19.8, "lowBattery": True}


def test_decode_5() -> None:
    decoded = weather20.decode(
        "0302020302020202030303020302020202020202030302020203020302020202020202020104"
    )
    assert decoded == {"id": 2318, "unit": 1, "temperature": 19.7, "lowBattery": True}


def test_decode_6() -> None:
    decoded = weather20.decode(
        "0302020302020202030303020302020202020202030302020202020302020202020202020104"
    )
    assert decoded == {"id": 2318, "unit": 1, "temperature": 19.3, "lowBattery": True}


def test_decode_7() -> None:
    decoded = weather20.decode(
        "0302020302020202030303020302020202020202030302020302020202020202020202020104"
    )
    assert decoded == {"id": 2318, "unit": 1, "temperature": 20.0, "lowBattery": True}
