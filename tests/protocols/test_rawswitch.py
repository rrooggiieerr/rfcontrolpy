import logging

from rfcontrol.protocols import rawswitch

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_is_not_supported() -> None:
    assert rawswitch.decode("0102") is None


def test_encode_1() -> None:
    encoded = rawswitch.encode(
        pulse_lengths=[300, 900, 9000],
        pulses_on="0102010201020102010201020102010201020102",
        pulses_off="0201020102010201020102010201020102010201",
        state=False,
    )
    assert encoded == "0201020102010201020102010201020102010201"
    assert rawswitch.pulse_lengths == [300, 900, 9000]
