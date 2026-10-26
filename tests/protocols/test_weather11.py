import logging

from rfcontrol.protocols import weather11

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = weather11.decode(
        "020202010202010102010101010101020101010202010201020202020101020201020201010101010103"
    )
    assert decoded == {
        "id": 236,
        "unit": 1,
        "temperature": 28.2,
        "humidity": 54,
        "lowBattery": False,
    }
