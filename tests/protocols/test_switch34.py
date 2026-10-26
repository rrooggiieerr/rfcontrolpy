import logging

from rfcontrol.protocols import switch34

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch34.decode(
        "01010101101010011001010101011010010101011001010110010101010110010102"
    )
    assert decoded == {
        "bits": "000011101000001100001000100000100",
        "bytes": [14, 131, 8, 130],
        "id": 7430,
        "unit": 8,
        "all": True,
        "state": True,
    }


def test_encode_1() -> None:
    encoded = switch34.encode()
    assert (
        encoded
        == "01111111101010111011111111111010111111111010101010111111111011111112"
    )
