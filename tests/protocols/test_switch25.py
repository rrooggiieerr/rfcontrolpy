import logging

from rfcontrol.protocols import switch25

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch25.decode(
        "101010101010101010101010101010100101010101010101011010100110011002"
    )
    assert decoded == {"id": 0, "unit": 14, "state": True}


def test_decode_2() -> None:
    decoded = switch25.decode(
        "101010101010101010101010101010100101010101010101011010100101101002"
    )
    assert decoded == {"id": 0, "unit": 14, "state": False}


def test_decode_3() -> None:
    decoded = switch25.decode(
        "101010101010101010101010101010100101010101010101011001101010011002"
    )
    assert decoded == {"id": 0, "unit": 11, "state": True}


def test_decode_4() -> None:
    decoded = switch25.decode(
        "101010101010101010101010101010100101010101010101011001101001101002"
    )
    assert decoded == {"id": 0, "unit": 11, "state": False}


def test_decode_5() -> None:
    decoded = switch25.decode(
        "101010101010101010101010101010100101010101010101010110101010011002"
    )
    assert decoded == {"id": 0, "unit": 7, "state": True}


def test_decode_6() -> None:
    decoded = switch25.decode(
        "101010101010101010101010101010100101010101010101010110101001101002"
    )
    assert decoded == {"id": 0, "unit": 7, "state": False}


def test_decode_7() -> None:
    decoded = switch25.decode(
        "101010101010101010101010101010100101010101010101011010011010011002"
    )
    assert decoded == {"id": 0, "unit": 13, "state": True}


def test_decode_8() -> None:
    decoded = switch25.decode(
        "101010101010101010101010101010100101010101010101011010011001101002"
    )
    assert decoded == {"id": 0, "unit": 13, "state": False}


def test_decode_9() -> None:
    decoded = switch25.decode(
        "101010101010101010101010101010100101010101010101010101010110011002"
    )
    assert decoded == {"id": 0, "unit": 0, "state": True}


def test_decode_10() -> None:
    decoded = switch25.decode(
        "101010101010101010101010101010100101010101010101010101010101101002"
    )
    assert decoded == {"id": 0, "unit": 0, "state": False}


def test_encode_1() -> None:
    encoded = switch25.encode(id=0, unit=14, state=True)
    assert (
        encoded == "101010101010101010101010101010100101010101010101011010100110011002"
    )


def test_encode_2() -> None:
    encoded = switch25.encode(id=0, unit=14, state=False)
    assert (
        encoded == "101010101010101010101010101010100101010101010101011010100101101002"
    )


def test_encode_3() -> None:
    encoded = switch25.encode(id=0, unit=11, state=True)
    assert (
        encoded == "101010101010101010101010101010100101010101010101011001101010011002"
    )


def test_encode_4() -> None:
    encoded = switch25.encode(id=0, unit=11, state=False)
    assert (
        encoded == "101010101010101010101010101010100101010101010101011001101001101002"
    )


def test_encode_5() -> None:
    encoded = switch25.encode(id=0, unit=7, state=True)
    assert (
        encoded == "101010101010101010101010101010100101010101010101010110101010011002"
    )


def test_encode_6() -> None:
    encoded = switch25.encode(id=0, unit=7, state=False)
    assert (
        encoded == "101010101010101010101010101010100101010101010101010110101001101002"
    )


def test_encode_7() -> None:
    encoded = switch25.encode(id=0, unit=13, state=True)
    assert (
        encoded == "101010101010101010101010101010100101010101010101011010011010011002"
    )


def test_encode_8() -> None:
    encoded = switch25.encode(id=0, unit=13, state=False)
    assert (
        encoded == "101010101010101010101010101010100101010101010101011010011001101002"
    )


def test_encode_9() -> None:
    encoded = switch25.encode(id=0, unit=0, state=True)
    assert (
        encoded == "101010101010101010101010101010100101010101010101010101010110011002"
    )


def test_encode_10() -> None:
    encoded = switch25.encode(id=0, unit=0, state=False)
    assert (
        encoded == "101010101010101010101010101010100101010101010101010101010101101002"
    )
