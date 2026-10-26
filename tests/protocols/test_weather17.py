import logging

from rfcontrol.protocols import weather17

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = weather17.decode(
        "1111111101110111111111111111010111111111110101011111111111111101110101011111111101011112"
    )
    assert decoded == {"id": 24, "temperature": 20.1}


def test_decode_2() -> None:
    decoded = weather17.decode(
        "1111111101110111111111111111010111111101110101011111011101111111110101011111011101111112"
    )
    assert decoded == {"id": 24, "temperature": 22.8}


def test_decode_3() -> None:
    decoded = weather17.decode(
        "1111111101110111010101111111010111111101110101111111011111111111110101111111011101011112"
    )
    assert decoded == {"id": 24, "humidity": 62}


def test_decode_4() -> None:
    decoded = weather17.decode(
        "1111111101110111010101111111010111111101110101111111110111111111110101111111110101110112"
    )
    assert decoded == {"id": 24, "humidity": 61}
