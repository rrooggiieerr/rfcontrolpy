import logging

from rfcontrol.protocols import weather9

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    # A synthetic message, the original implementation has no test data for
    # weather9. The expected values are what the original implementation decodes.
    decoded = weather9.decode(
        "01010201010202010201020202020101020102010201010202020102010102020102020202010102010103"
    )
    assert decoded == {
        "id": 38,
        "unit": 4,
        "temperature": 40.8,
        "humidity": 212,
        "lowBattery": True,
        "sync": True,
    }
