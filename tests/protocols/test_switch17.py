import logging

from rfcontrol.protocols import switch17

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch17.decode(
        "020100010001000001000100010100010001000100010000010100000101000100010001000100010001000100000100010100000100010100010001000001010003"
    )
    assert decoded == {"id": 59748338, "all": False, "state": True, "unit": 13}


def test_encode_1() -> None:
    encoded = switch17.encode(id=9969333, unit=1, state=True, all=True)
    assert (
        encoded
        == "020001000101000001000101000100000100010001000100010001010001000100010000010100000101000100000101000001010001000100000100010001010003"
    )
