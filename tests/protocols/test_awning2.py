import logging

from rfcontrol.protocols import awning2

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = awning2.decode(
        "3210101010011010010101101001010101100101011010100110011010010101100101011001010114"
    )
    assert decoded == {"id": 2065188696, "command": "in"}


def test_encode_1() -> None:
    encoded = awning2.encode(id=75003370, command="stop")
    assert (
        encoded
        == "3201010101100101011010101001010101101010011001101010100110011001100110011001100114"
    )
