import logging

from rfcontrol.protocols import switch30

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch30.decode("01010101010110100101101001001110101001010101010102")
    assert decoded == {"id": 21850, "unit": 23118, "command": "arm"}


def test_decode_2() -> None:
    decoded = switch30.decode("01010101010110100101101001001110010101011010010102")
    assert decoded == {"id": 21850, "unit": 23118, "command": "dis"}


def test_decode_3() -> None:
    decoded = switch30.decode("01010101010110100101101001001110010101010101101002")
    assert decoded == {"id": 21850, "unit": 23118, "command": "byp"}


def test_decode_4() -> None:
    decoded = switch30.decode("01010101010110100101101001001110010110100101010102")
    assert decoded == {"id": 21850, "unit": 23118, "command": "sos"}


def test_encode_1() -> None:
    encoded = switch30.encode(id=21850, unit=23118, command="arm")
    assert encoded == "01010101010110100101101001001110101001010101010102"
