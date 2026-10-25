import logging

from rfcontrol.protocols import switch11

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch11.decode(
        "100101010110011010101001101001010101100110010110011010100110011002"
    )
    assert decoded == {"id": 34037, "unit": 1, "state": True}


def test_decode_2() -> None:
    decoded = switch11.decode(
        "100101011010011010101001101001010101100110010110011010100110011002"
    )
    assert decoded == {"id": 34037, "unit": 1, "state": False}


def test_decode_3() -> None:
    decoded = switch11.decode(
        "100101101001011010101001101001010101100110010110011010100110011002"
    )
    assert decoded == {"id": 34037, "unit": 0, "state": True}


def test_decode_4() -> None:
    decoded = switch11.decode(
        "100101100110011010101001101001010101100110010110011010100110011002"
    )
    assert decoded == {"id": 34037, "unit": 0, "state": False}


def test_encode_1() -> None:
    encoded = switch11.encode(id=34037, unit=1, state=True)
    assert (
        encoded == "100101010110011010101001101001010101100110010110011010100110011002"
    )


def test_encode_2() -> None:
    encoded = switch11.encode(id=34037, unit=1, state=False)
    assert (
        encoded == "100101011010011010101001101001010101100110010110011010100110011002"
    )


def test_encode_3() -> None:
    encoded = switch11.encode(id=34037, unit=0, state=True)
    assert (
        encoded == "100101101001011010101001101001010101100110010110011010100110011002"
    )


def test_encode_4() -> None:
    encoded = switch11.encode(id=34037, unit=0, state=False)
    assert (
        encoded == "100101100110011010101001101001010101100110010110011010100110011002"
    )
