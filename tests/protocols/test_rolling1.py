import logging

from rfcontrol.protocols import rolling1

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = rolling1.decode("01101010100101011001101010010110100110100101100123")
    assert decoded == {"code": "011110001011100110110010"}


def test_decode_2() -> None:
    decoded = rolling1.decode("01101010011010011010011010010101100110011010100123")
    assert decoded == {"code": "011101101101100010101110"}


def test_decode_3() -> None:
    decoded = rolling1.decode("01101010011010011010011010010101100110011010010123")
    assert decoded == {"code": "011101101101100010101100"}


def test_encode_1() -> None:
    encoded = rolling1.encode(
        code_on=[
            "011111110000111001011100",
            "011101101101100010101100",
            "011111011110001001101100",
            "011110011010111100011100",
        ],
        code_off=[
            "011110001011100110111100",
            "011110101001110001111100",
            "011100010001011100101100",
            "011101110011101010001100",
        ],
        state=True,
    )
    assert encoded == "01101010101010100101010110101001011001101010010123"
