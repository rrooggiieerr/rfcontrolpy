import logging

from rfcontrol.protocols import weather3

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = weather3.decode(
        "01010202020201020201010102010102020201020202010202010201010101010202010201010101020103"
    )
    assert decoded == {"id": 246, "unit": 3, "temperature": 24.2, "humidity": 56}


def test_decode_2() -> None:
    decoded = weather3.decode(
        "01010202020201020201010102010201020201020202010202010201010101010202010201010202010103"
    )
    assert decoded == {"id": 246, "unit": 3, "temperature": 24.4, "humidity": 56}


def test_decode_3() -> None:
    decoded = weather3.decode(
        "01010201020102020102010101010101010101020101010202010101010201020101010101010102010203"
    )
    assert decoded == {"id": 173, "unit": 1, "temperature": 21.1, "humidity": 65}


def test_decode_4() -> None:
    decoded = weather3.decode(
        "01010201020102020102010101010102020201020101010202010101010201020101010101010102010103"
    )
    assert decoded == {"id": 173, "unit": 1, "temperature": 21.5, "humidity": 65}


def test_decode_5() -> None:
    decoded = weather3.decode(
        "01010101010202020201010101020201010201010101010202010202020101010202010201010101010203"
    )
    assert decoded == {"id": 30, "unit": 2, "temperature": 18.1, "humidity": 62}


def test_decode_6() -> None:
    decoded = weather3.decode(
        "01010101010202020201010101020102010201010102010202010202020201010202010101010202010103"
    )
    assert decoded == {"id": 30, "unit": 2, "temperature": 18.7, "humidity": 63}
