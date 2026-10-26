import logging

from rfcontrol.protocols import switch13

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch13.decode("001100110101001010101010101010110010101102")
    assert decoded == {
        "id": 1472,
        "unit": 0,
        "all": False,
        "state": True,
        "dimm": False,
    }


def test_decode_2() -> None:
    decoded = switch13.decode("001100110101001010101010101010101010101012")
    assert decoded == {
        "id": 1472,
        "unit": 0,
        "all": False,
        "state": False,
        "dimm": False,
    }


def test_decode_3() -> None:
    decoded = switch13.decode("001100110101001010101010101010101100110012")
    assert decoded == {
        "id": 1472,
        "unit": 0,
        "all": False,
        "state": False,
        "dimm": True,
    }


def test_decode_4() -> None:
    decoded = switch13.decode("001100110101001010101010101010110100110102")
    assert decoded == {"id": 1472, "unit": 0, "all": False, "state": True, "dimm": True}


def test_encode_1() -> None:
    encoded = switch13.encode(id=1472, unit=0, all=False, state=True, dimm=False)
    assert encoded == "001100110101001010101010101010110010101102"
