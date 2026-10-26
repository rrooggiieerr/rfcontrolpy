import logging

from rfcontrol.protocols import weather6

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = weather6.decode(
        "01020102010202020101010101010101010201020201020102010102020101020102020101030103"
    )
    assert decoded == {
        "id": 87,
        "unit": 1,
        "temperature": 9.0,
        "humidity": 76,
        "lowBattery": True,
    }
