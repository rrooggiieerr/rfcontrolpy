import logging

from rfcontrol.protocols import pir5

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = pir5.decode(
        "0200010001010001000001000100010100010000010100010001000100010000010100000100010001010001000001010001000001000101000100000100010100000101000001000103"
    )
    assert decoded == {"id": 13040182, "all": False, "state": True, "unit": 9}
