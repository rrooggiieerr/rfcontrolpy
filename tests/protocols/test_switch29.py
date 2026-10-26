import logging

from rfcontrol.protocols import switch29

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch29.decode(
        "00101011101010101101001010101010111000110010101010110010101011001011010102"
    )
    assert decoded == {"id": 5723557, "unit": 5621333, "command": "arm"}


def test_decode_2() -> None:
    decoded = switch29.decode(
        "00101011101010101101001010101010111000110010101010101011001011001010110012"
    )
    assert decoded == {"id": 5723557, "unit": 5621333, "command": "panic"}


def test_decode_3() -> None:
    decoded = switch29.decode(
        "00101011101010101101001010101010111000110010101011001010101011001100110102"
    )
    assert decoded == {"id": 5723557, "unit": 5621333, "command": "disarm"}


def test_decode_4() -> None:
    decoded = switch29.decode(
        "00101011101010101101001010101010111000110010101010101100101011001010101102"
    )
    assert decoded == {"id": 5723557, "unit": 5621333, "command": "home"}


def test_decode_5() -> None:
    decoded = switch29.decode(
        "00101011101010101101001010101010111000110010101011010010101011001101010102"
    )
    assert decoded == {"id": 5723557, "unit": 5621333, "command": "grp1"}


def test_decode_6() -> None:
    decoded = switch29.decode(
        "00101011101010101101001010101010111000110010101011001100101011001100101102"
    )
    assert decoded == {"id": 5723557, "unit": 5621333, "command": "grp2"}


def test_decode_7() -> None:
    decoded = switch29.decode(
        "00101011101010101101001010101010111000110010101011010100101011001101001102"
    )
    assert decoded == {"id": 5723557, "unit": 5621333, "command": "grp3"}


def test_encode_1() -> None:
    encoded = switch29.encode(id=5723557, unit=5621333, command="panic")
    assert (
        encoded
        == "00101011101010101101001010101010111000110010101010101011001011001010110012"
    )
