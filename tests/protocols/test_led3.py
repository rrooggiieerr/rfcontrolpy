import logging

from rfcontrol.protocols import led3

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = led3.decode("01011010011010100110010110010101010101010101011002")
    assert decoded == {"id": 14152, "command": "on/off"}


def test_encode_1() -> None:
    encoded = led3.encode(id=14152, command="cyan")
    assert encoded == "01011010011010100110010110010101010101100110010102"
