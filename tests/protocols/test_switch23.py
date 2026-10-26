import logging

from rfcontrol.protocols import switch23

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch23.decode("00110011001100110011010100110011001012")
    assert decoded == {"id": 10914, "command": "C"}


def test_decode_2() -> None:
    decoded = switch23.decode("00110011001100110011010100110011010012")
    assert decoded == {"id": 10914, "command": "D"}


def test_decode_3() -> None:
    decoded = switch23.decode("00110011001100110011010100110010101102")
    assert decoded == {"id": 10914, "command": "A"}


def test_decode_4() -> None:
    decoded = switch23.decode("00110011001100110011010100110010110102")
    assert decoded == {"id": 10914, "command": "B"}


def test_encode_1() -> None:
    encoded = switch23.encode(id=8438, command="E")
    assert encoded == "00110101010100101010110010110010101102"
