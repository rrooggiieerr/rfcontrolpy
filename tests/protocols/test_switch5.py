import logging

from rfcontrol.protocols import switch5

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch5.decode("10010101101010010110010110101001010101011010101002")
    assert decoded == {"id": 465695, "unit": 1, "all": False, "state": True}


def test_decode_2() -> None:
    decoded = switch5.decode("10010101101010010110010110101001010101011010100102")
    assert decoded == {"id": 465695, "unit": 1, "all": False, "state": False}


def test_decode_3() -> None:
    decoded = switch5.decode("10010101101010010110010110101001010101011010011002")
    assert decoded == {"id": 465695, "unit": 2, "all": False, "state": True}


def test_decode_4() -> None:
    decoded = switch5.decode("10010101101010010110010110101001010101011010010102")
    assert decoded == {"id": 465695, "unit": 2, "all": False, "state": False}


def test_decode_5() -> None:
    decoded = switch5.decode("10010101101010010110010110101001010101011001101002")
    assert decoded == {"id": 465695, "unit": 3, "all": False, "state": True}


def test_decode_6() -> None:
    decoded = switch5.decode("10010101101010010110010110101001010101011001100102")
    assert decoded == {"id": 465695, "unit": 3, "all": False, "state": False}


def test_decode_7() -> None:
    decoded = switch5.decode("10010101101010010110010110101001010101010110101002")
    assert decoded == {"id": 465695, "unit": 4, "all": False, "state": True}


def test_decode_8() -> None:
    decoded = switch5.decode("10010101101010010110010110101001010101010110100102")
    assert decoded == {"id": 465695, "unit": 4, "all": False, "state": False}


def test_decode_9() -> None:
    decoded = switch5.decode("10010101101010010110010110101001010101010101011002")
    assert decoded == {"id": 465695, "unit": 0, "all": True, "state": False}


def test_decode_10() -> None:
    decoded = switch5.decode("10010101101010010110010110101001010101010101100102")
    assert decoded == {"id": 465695, "unit": 0, "all": True, "state": True}


def test_encode_1() -> None:
    encoded = switch5.encode(id=465695, unit=1, all=False, state=True)
    assert encoded == "10010101101010010110010110101001010101011010101002"


def test_encode_2() -> None:
    encoded = switch5.encode(id=465695, unit=1, all=False, state=False)
    assert encoded == "10010101101010010110010110101001010101011010100102"


def test_encode_3() -> None:
    encoded = switch5.encode(id=465695, unit=2, all=False, state=True)
    assert encoded == "10010101101010010110010110101001010101011010011002"


def test_encode_4() -> None:
    encoded = switch5.encode(id=465695, unit=2, all=False, state=False)
    assert encoded == "10010101101010010110010110101001010101011010010102"


def test_encode_5() -> None:
    encoded = switch5.encode(id=465695, unit=3, all=False, state=True)
    assert encoded == "10010101101010010110010110101001010101011001101002"


def test_encode_6() -> None:
    encoded = switch5.encode(id=465695, unit=3, all=False, state=False)
    assert encoded == "10010101101010010110010110101001010101011001100102"


def test_encode_7() -> None:
    encoded = switch5.encode(id=465695, unit=4, all=False, state=True)
    assert encoded == "10010101101010010110010110101001010101010110101002"


def test_encode_8() -> None:
    encoded = switch5.encode(id=465695, unit=4, all=False, state=False)
    assert encoded == "10010101101010010110010110101001010101010110100102"


def test_encode_9() -> None:
    encoded = switch5.encode(id=465695, unit=0, all=True, state=False)
    assert encoded == "10010101101010010110010110101001010101010101011002"


def test_encode_10() -> None:
    encoded = switch5.encode(id=465695, unit=0, all=True, state=True)
    assert encoded == "10010101101010010110010110101001010101010101100102"
