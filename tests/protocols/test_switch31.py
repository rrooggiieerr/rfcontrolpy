import logging

from rfcontrol.protocols import switch31

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch31.decode(
        "0000220100010101000000010101000001000100010000000101010000000101000100010000000001010103"
    )
    assert decoded == {"id": 47333, "unit": 1, "state": True, "all": False}


def test_decode_2() -> None:
    decoded = switch31.decode(
        "0000220100010101000000010101000001000100010000000101010000000101000100000101010100000003"
    )
    assert decoded == {"id": 47333, "unit": 1, "state": False, "all": False}


def test_decode_3() -> None:
    decoded = switch31.decode(
        "0000220100010101000000010101000001000100010000000101010000000101000100000100000100010103"
    )
    assert decoded == {"id": 47333, "unit": 2, "state": True, "all": False}


def test_decode_4() -> None:
    decoded = switch31.decode(
        "0000220100010101000000010101000001000100010000000101010000000101000100010001010001000003"
    )
    assert decoded == {"id": 47333, "unit": 2, "state": False, "all": False}


def test_decode_5() -> None:
    decoded = switch31.decode(
        "0000220100010101000000010101000001000100010000000101010000000101000100010100000000010103"
    )
    assert decoded == {"id": 47333, "unit": 3, "state": True, "all": False}


def test_decode_6() -> None:
    decoded = switch31.decode(
        "0000220100010101000000010101000001000100010000000101010000000101000100000001010101000003"
    )
    assert decoded == {"id": 47333, "unit": 3, "state": False, "all": False}


def test_decode_7() -> None:
    decoded = switch31.decode(
        "0000220100010101000000010101000001000100010000000101010000000101000100000001000101000103"
    )
    assert decoded == {"id": 47333, "unit": 4, "state": True, "all": False}


def test_decode_8() -> None:
    decoded = switch31.decode(
        "0000220100010101000000010101000001000100010000000101010000000101000100010100010000010003"
    )
    assert decoded == {"id": 47333, "unit": 4, "state": False, "all": False}


def test_decode_9() -> None:
    decoded = switch31.decode(
        "0000220100010101000000010101000001000100010000000101010000000101000100010001000001000103"
    )
    assert decoded == {"id": 47333, "unit": 5, "state": True, "all": True}


def test_decode_10() -> None:
    decoded = switch31.decode(
        "0000220100010101000000010101000001000100010000000101010000000101000100000100010100010003"
    )
    assert decoded == {"id": 47333, "unit": 5, "state": False, "all": True}


def test_encode_1() -> None:
    encoded = switch31.encode(all=False, unit=1, id=47333, state=True)
    assert (
        encoded
        == "0000220100010101000000010101000001000100010000000101010000000101000100010000000001010103"
    )
