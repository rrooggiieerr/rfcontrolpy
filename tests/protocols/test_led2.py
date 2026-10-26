import logging

from rfcontrol.protocols import led2

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = led2.decode("01010110101001101010100110011001010101100101011002")
    assert decoded == {"id": 7658, "command": "mode-"}


def test_decode_2() -> None:
    decoded = led2.decode("01010110101001101010100110011001010101011001011002")
    assert decoded == {"id": 7658, "command": "25%"}


def test_decode_3() -> None:
    decoded = led2.decode("01010110101001101010100110011001010101010110101002")
    assert decoded == {"id": 7658, "command": "100%"}


def test_decode_4() -> None:
    decoded = led2.decode("01010110101001101010100110011001010101010101011002")
    assert decoded == {"id": 7658, "command": "on/off"}


def test_decode_5() -> None:
    decoded = led2.decode("01010110101001101010100110011001010110010101011002")
    assert decoded == {"id": 7658, "command": "code:00100001"}


def test_encode_1() -> None:
    encoded = led2.encode(id=2019, command="on/off")
    assert encoded == "01010101011010101010100101011010010101010101011002"
