import logging

from rfcontrol.protocols import weather10

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = weather10.decode(
        "01010102020202010201010101010101020202010201020102020202010101010101010103"
    )
    assert decoded == {"id": 122, "unit": 1, "temperature": 23.4}
