import logging

from rfcontrol.protocols import switch9

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch9.decode("0110100101100110011010101001101010101001011012")
    assert decoded == {"id": 2472, "unit": 65, "state": True}


def test_decode_2() -> None:
    decoded = switch9.decode("0110100101100110011010101001101010101001101012")
    assert decoded == {"id": 2472, "unit": 65, "state": False}


def test_decode_3() -> None:
    decoded = switch9.decode("0110100101100110011010101001101010101010011012")
    assert decoded == {"id": 2472, "unit": 64, "state": True}


def test_decode_4() -> None:
    decoded = switch9.decode("0110100101100110011010101001101010010101100112")
    assert decoded == {"id": 2472, "unit": 71, "state": False}


def test_encode_1() -> None:
    encoded = switch9.encode(id=2472, unit=65, state=True)
    assert encoded == "0110100101100110011010101001101010101001011012"
