import logging

from rfcontrol.protocols import weather18

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = weather18.decode(
        "0101020102020102020101010101010102020201010102020202020201020202010202020003"
    )
    assert decoded == {"id": 45, "unit": 1, "temperature": 22.7}


def test_decode_2() -> None:
    decoded = weather18.decode(
        "0101020102020102020101010101010102020202010102020202020201010102020101020003"
    )
    assert decoded == {"id": 45, "unit": 1, "temperature": 24.3}


def test_decode_3() -> None:
    decoded = weather18.decode(
        "0101020102020102020101010101010201010201010101010202020202010202010202010003"
    )
    assert decoded == {"id": 45, "unit": 1, "temperature": 28.8}


def test_decode_4() -> None:
    decoded = weather18.decode(
        "0101020102020102020101010101010201010102010101010202020201010101010201010003"
    )
    assert decoded == {"id": 45, "unit": 1, "temperature": 27.2}
