import logging

from rfcontrol.protocols import rawshutter

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_is_not_supported() -> None:
    assert rawshutter.decode("0102") is None


def test_encode_1() -> None:
    encoded = rawshutter.encode(
        pulse_lengths=[300, 900],
        pulses_up="01",
        pulses_down="10",
        pulses_stop="11",
        command="down",
    )
    assert encoded == "10"
    assert rawshutter.pulse_lengths == [300, 900]
