import logging

import pytest

from rfcontrol.protocols import dimmer1, switch1

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = dimmer1.decode(
        "0200010001010000010001010000010001000101000100010001000100000101000100010000010001000100010001010001000001000100000001000100010001010001000100010003"
    )
    assert decoded == {
        "id": 9565958,
        "all": False,
        "state": None,
        "unit": 0,
        "dimlevel": 15,
    }


def test_decode_2() -> None:
    decoded = dimmer1.decode(
        "0200010001010000010001010000010001000101000100010001000100000101000100010000010001000100010001010001000001000101000001000100010001010001000100010003"
    )
    assert decoded == {
        "id": 9565958,
        "all": False,
        "state": True,
        "unit": 0,
        "dimlevel": 15,
    }


def test_encode_1() -> None:
    encoded = dimmer1.encode(unit=0, id=9565958, all=False, state=None, dimlevel=15)
    assert (
        encoded
        == "0200010001010000010001010000010001000101000100010001000100000101000100010000010001000100010001010001000001000100000001000100010001010001000100010003"
    )

    # 020001000101000001000101000001000100010100010001000100010000010100010001000001000100010001000101000100000100000001000100010001010001000100010003
    # 0200010001010000010001010000010001000101000100010001000100000101000100010000010001000100010001010001000001000100000001000100010001010001000100010003


def test_encode_without_dimlevel() -> None:
    # Without a dim level a plain on/off message is sent, the same as switch1.
    for state in (True, False):
        encoded = dimmer1.encode(id=9565958, unit=0, state=state)
        assert encoded == switch1.encode(id=9565958, unit=0, state=state)
        assert switch1.decode(encoded) == {
            "id": 9565958,
            "unit": 0,
            "all": False,
            "state": state,
        }


def test_encode_without_state_and_dimlevel() -> None:
    with pytest.raises(ValueError, match="Either state or dimlevel is required"):
        dimmer1.encode(id=9565958, unit=0)
