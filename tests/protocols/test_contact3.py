import logging

from rfcontrol.protocols import contact3

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    # A synthetic message, the original implementation has no test data for
    # contact3. The expected values are what the original implementation decodes.
    decoded = contact3.decode("10011001101001100101011010010110011001011001101002")
    assert decoded == {"id": 339563, "state": False}
