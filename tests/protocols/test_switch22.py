import logging

from rfcontrol.protocols import switch22

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch22.decode("01100110101010101001100101010101101010010101011002")
    assert decoded == {"id": 656881, "command": "A"}


def test_decode_2() -> None:
    decoded = switch22.decode("01100110101010101001100101010101101010010101100102")
    assert decoded == {"id": 656881, "command": "B"}


def test_decode_3() -> None:
    decoded = switch22.decode("01100110101010101001100101010101101010010110010102")
    assert decoded == {"id": 656881, "command": "C"}


def test_decode_4() -> None:
    decoded = switch22.decode("01100110101010101001100101010101101010011001010102")
    assert decoded == {"id": 656881, "command": "D"}


def test_encode_1() -> None:
    encoded = switch22.encode(id=71900, command="A")
    assert encoded == "10101001101010010110101001011001010110100101011002"
