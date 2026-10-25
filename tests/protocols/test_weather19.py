import logging

from rfcontrol.protocols import weather19

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = weather19.decode(
        "020202010101010101010101010101020101010102010201020101010201020203"
    )
    assert decoded == {"id": 56, "unit": 1, "temperature": 26.6}


def test_decode_2() -> None:
    decoded = weather19.decode(
        "020102020102010101010101010101020101020101020201010102020201020203"
    )
    assert decoded == {"id": 45, "unit": 1, "temperature": 29.4}


def test_decode_3() -> None:
    decoded = weather19.decode(
        "020102020102010101010101010101020101020201010101020102010102010203"
    )
    assert decoded == {"id": 45, "unit": 1, "temperature": 30.4}


def test_decode_4() -> None:
    decoded = weather19.decode(
        "020102020102010101010101010101020202010102020101020102010101010203"
    )
    assert decoded == {"id": 45, "unit": 1, "temperature": 46.0}
