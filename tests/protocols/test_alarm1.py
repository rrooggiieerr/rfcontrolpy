import logging

from rfcontrol.protocols import alarm1

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = alarm1.decode("3002020101010102020201010101020101010102020202010204")
    assert decoded == {"id": 12813373, "state": True}


def test_encode_1() -> None:
    encoded = alarm1.encode(id=16214399, state=False)
    assert encoded == "0"
