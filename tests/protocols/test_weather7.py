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


def test_decode_negative_temperature() -> None:
    # Synthetic: the first test's capture with the temperature set to -3.0,
    # checked against the original implementation.
    decoded = weather7.decode(
        "010202010201010202010101020202020202020101010201020202010202010103"
    )
    assert decoded == {
        "id": 105,
        "unit": 0,
        "temperature": -3.0,
        "humidity": 59,
        "lowBattery": False,
    }
