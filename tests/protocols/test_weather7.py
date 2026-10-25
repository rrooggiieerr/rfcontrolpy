import logging

from rfcontrol.protocols import weather7

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = weather7.decode(
        "010202010201010202010101010101010101010202020102020202010202010103"
    )
    assert decoded == {
        "id": 105,
        "unit": 0,
        "temperature": 2.9,
        "humidity": 59,
        "lowBattery": False,
    }
