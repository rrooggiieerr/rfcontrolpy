import logging

from rfcontrol.protocols import pir3

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = pir3.decode(
        "100110100110011001100110101001101010011001100110100101100101101002"
    )
    assert decoded == {"id": 19106, "unit": 10860, "state": True}
