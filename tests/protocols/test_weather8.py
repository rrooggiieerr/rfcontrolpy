import logging

from rfcontrol.protocols import weather8

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = weather8.decode(
        "01010101020202010202020202020202020201010102010102020202010202020101020103"
    )
    assert decoded == {"id": 14, "temperature": -14.2, "humidity": 196}
