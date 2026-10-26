import logging

from rfcontrol.protocols import switch19

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch19.decode("10010101101010010110010110101001010101011010101002")
    assert decoded == {"id": None, "unit": None, "state": None}


def test_encode_1() -> None:
    encoded = switch19.encode(id="D", unit=1, state=True)
    assert encoded == "01100110011001101010011001100101010101011010010102"
