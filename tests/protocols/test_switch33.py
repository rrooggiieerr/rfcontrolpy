import logging

from rfcontrol.protocols import switch33

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch33.decode("010011010010101010101010101100110010101012")
    assert decoded == {
        "id": 2816,
        "unit": 1,
        "all": False,
        "state": True,
        "dimm": False,
    }


def test_decode_2() -> None:
    decoded = switch33.decode("010011010010101010101010110010110010110102")
    assert decoded == {
        "id": 2816,
        "unit": 2,
        "all": False,
        "state": True,
        "dimm": False,
    }


def test_decode_3() -> None:
    decoded = switch33.decode("010011010010101010101010110010101010110012")
    assert decoded == {
        "id": 2816,
        "unit": 2,
        "all": False,
        "state": False,
        "dimm": False,
    }


def test_decode_4() -> None:
    decoded = switch33.decode("010011010010101010101010110100110010110012")
    assert decoded == {
        "id": 2816,
        "unit": 3,
        "all": False,
        "state": True,
        "dimm": False,
    }


def test_decode_5() -> None:
    decoded = switch33.decode("010011010010101010101010110100101010110102")
    assert decoded == {
        "id": 2816,
        "unit": 3,
        "all": False,
        "state": False,
        "dimm": False,
    }


def test_decode_6() -> None:
    decoded = switch33.decode("010011010010101010101010110101010010101012")
    assert decoded == {"id": 2816, "unit": 3, "all": True, "state": True, "dimm": False}


def test_decode_7() -> None:
    decoded = switch33.decode("010011010010101010101010110101001010101102")
    assert decoded == {
        "id": 2816,
        "unit": 3,
        "all": True,
        "state": False,
        "dimm": False,
    }


def test_decode_8() -> None:
    decoded = switch33.decode("010011010010101010101010110101010100110012")
    assert decoded == {"id": 2816, "unit": 3, "all": True, "state": True, "dimm": True}


def test_decode_9() -> None:
    decoded = switch33.decode("010011010010101010101010110101001100110102")
    assert decoded == {"id": 2816, "unit": 3, "all": True, "state": False, "dimm": True}


def test_encode_1() -> None:
    encoded = switch33.encode(id=3823, unit=0, state=False, all=True, dimm=True)
    assert encoded == "010101001101010011010101001011001100101012"
