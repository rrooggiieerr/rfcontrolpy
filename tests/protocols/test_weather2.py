import logging

from rfcontrol.protocols import weather2

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = weather2.decode(
        "01010102020202010201010101010101020202010201020102020202010101010101010103"
    )
    assert decoded == {"temperature": 23.4}


def test_decode_2() -> None:
    decoded = weather2.decode(
        "01010102020202010201010101010101020202010201010202020202010101010101010103"
    )
    assert decoded == {"temperature": 23.3}


def test_decode_3() -> None:
    decoded = weather2.decode(
        "01010102020202010201010101010101020202010201010102020202010101010101010103"
    )
    assert decoded == {"temperature": 23.2}


def test_decode_4() -> None:
    decoded = weather2.decode(
        "01010101020201020201010101010102010101010202010102020202010101010101010103"
    )
    assert decoded == {"temperature": 26.8}


def test_decode_5() -> None:
    decoded = weather2.decode(
        "01010101020201020201010101010102010101010201010102020202010101010101010103"
    )
    assert decoded == {"temperature": 26.4}


def test_decode_6() -> None:
    decoded = weather2.decode(
        "02010102010102020201010102020202020102020102020102020202010101010202020103"
    )
    assert decoded == {"temperature": -7.4}
