import logging

from rfcontrol.protocols import doorbell3

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = doorbell3.decode("00101010101010101100110012")
    assert decoded == {"id": 0, "unit": 10}


def test_decode_2() -> None:
    decoded = doorbell3.decode("01010010101010101100110012")
    assert decoded == {"id": 12, "unit": 10}


def test_decode_3() -> None:
    decoded = doorbell3.decode("00110010101010101100110012")
    assert decoded == {"id": 4, "unit": 10}


def test_decode_4() -> None:
    decoded = doorbell3.decode("01010101001010101100110012")
    assert decoded == {"id": 15, "unit": 10}


def test_decode_5() -> None:
    decoded = doorbell3.decode("00110101001010101100110012")
    assert decoded == {"id": 7, "unit": 10}


def test_decode_6() -> None:
    decoded = doorbell3.decode("01001101001010101100110012")
    assert decoded == {"id": 11, "unit": 10}


def test_decode_7() -> None:
    decoded = doorbell3.decode("00101101001010101100110012")
    assert decoded == {"id": 3, "unit": 10}


def test_decode_8() -> None:
    decoded = doorbell3.decode("01001100101010101100110012")
    assert decoded == {"id": 10, "unit": 10}


def test_decode_9() -> None:
    decoded = doorbell3.decode("00101100101010101100110012")
    assert decoded == {"id": 2, "unit": 10}


def test_decode_10() -> None:
    decoded = doorbell3.decode("01010100101010101100110012")
    assert decoded == {"id": 14, "unit": 10}


def test_decode_11() -> None:
    decoded = doorbell3.decode("00110100101010101100110012")
    assert decoded == {"id": 6, "unit": 10}


def test_decode_12() -> None:
    decoded = doorbell3.decode("01010011001010101100110012")
    assert decoded == {"id": 13, "unit": 10}


def test_decode_13() -> None:
    decoded = doorbell3.decode("00110011001010101100110012")
    assert decoded == {"id": 5, "unit": 10}


def test_decode_14() -> None:
    decoded = doorbell3.decode("01001011001010101100110012")
    assert decoded == {"id": 9, "unit": 10}


def test_decode_15() -> None:
    decoded = doorbell3.decode("00101011001010101100110012")
    assert decoded == {"id": 1, "unit": 10}


def test_decode_16() -> None:
    decoded = doorbell3.decode("01001010101010101100110012")
    assert decoded == {"id": 8, "unit": 10}


def test_encode_1() -> None:
    encoded = doorbell3.encode(id=1, unit=196)
    assert encoded == "00101011010100101011001012"
