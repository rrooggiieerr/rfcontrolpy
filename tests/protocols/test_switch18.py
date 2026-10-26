import logging

from rfcontrol.protocols import switch18

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch18.decode(
        "10011001010110101010011001011010100101010110010101010101101001010203"
    )
    assert decoded == {"id": 204241907, "state": False}


def test_encode_1() -> None:
    encoded = switch18.encode(id=226921516, state=True)
    assert (
        encoded == "100110010101100101101010100101100110101001011010101001100101101003"
    )
