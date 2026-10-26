import logging

from rfcontrol.protocols import led4

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = led4.decode("01010101010110100101011010100101100101010110011102")
    assert decoded == {"id": 796, "command": "on/off"}


def test_decode_2() -> None:
    decoded = led4.decode("01010101010110100101011010100101100101010101101102")
    assert decoded == {"id": 796, "command": "bright+"}


def test_decode_3() -> None:
    decoded = led4.decode("01010101010110100101011010100101100101010110100102")
    assert decoded == {"id": 796, "command": "color+"}


def test_decode_4() -> None:
    decoded = led4.decode("01010101010110100101011010100101010101101010011102")
    assert decoded == {"id": 796, "command": "code:00011101"}


def test_decode_5() -> None:
    decoded = led4.decode("01010101010110100101011010100101010101010110010102")
    assert decoded == {"id": 796, "command": "code:00000100"}


def test_encode_1() -> None:
    encoded = led4.encode(id=796, command="on/off")
    assert encoded == "01010101010110100101011010100101100101010110011002"
