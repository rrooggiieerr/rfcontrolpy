import logging

from rfcontrol.protocols import contact4

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_open_1() -> None:
    decoded = contact4.decode("10010110011001011010011010101001010101011010100102")
    assert decoded is not None
    assert decoded == {"id": 609760, "state": True, "lowBattery": False}


def test_decode_open_2() -> None:
    decoded = contact4.decode("10101001100110011001011010100101010101011010100102")
    assert decoded is not None
    assert decoded == {"id": 960960, "state": True, "lowBattery": False}


def test_decode_open_3() -> None:
    decoded = contact4.decode("01011010101001010110010110010101010101011010100102")
    assert decoded is not None
    assert decoded == {"id": 246912, "state": True, "lowBattery": False}


def test_decode_close_1() -> None:
    decoded = contact4.decode("10010110011001011010011010101001010101011001100102")
    assert decoded is not None
    assert decoded == {"id": 609760, "state": False, "lowBattery": False}


def test_decode_close_2() -> None:
    decoded = contact4.decode("10101001100110011001011010100101010101011001100102")
    assert decoded is not None
    assert decoded == {"id": 960960, "state": False, "lowBattery": False}


def test_decode_close_3() -> None:
    decoded = contact4.decode("01011010101001010110010110010101010101011001100102")
    assert decoded is not None
    assert decoded == {"id": 246912, "state": False, "lowBattery": False}


def test_decode_open_lowbattery() -> None:
    decoded = contact4.decode("10101001100110011001011010100101010101010110100102")
    assert decoded is not None
    assert decoded == {"id": 960960, "state": True, "lowBattery": True}


def test_encode_open_1() -> None:
    encoded = contact4.encode(id=609760, state=True, low_battery=False)
    assert encoded == "10010110011001011010011010101001010101011010100102"


def test_encode_open_2() -> None:
    encoded = contact4.encode(id=960960, state=True, low_battery=False)
    assert encoded == "10101001100110011001011010100101010101011010100102"


def test_encode_close_1() -> None:
    encoded = contact4.encode(id=609760, state=False, low_battery=False)
    assert encoded == "10010110011001011010011010101001010101011001100102"


def test_encode_close_2() -> None:
    encoded = contact4.encode(id=960960, state=False, low_battery=False)
    assert encoded == "10101001100110011001011010100101010101011001100102"


def test_encode_open_lowbattery() -> None:
    encoded = contact4.encode(id=960960, state=True, low_battery=True)
    assert encoded == "10101001100110011001011010100101010101010110100102"
