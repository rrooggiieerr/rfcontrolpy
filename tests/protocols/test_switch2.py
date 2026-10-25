import logging

from rfcontrol.protocols import switch2

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_decode_1() -> None:
    decoded = switch2.decode("01010101011001100101010101100110011001100101011002")
    assert decoded == {"id": 25, "unit": 16, "state": True}


# def test_decode_2() -> None:
#     decoded = switch2.decode('01100110011001100110010101010101010101010110010102')
#     assert decoded == {'unit': 0, 'id': 31, 'state': False}


# def test_decode_3() -> None:
#     decoded = switch2.decode('01010110010101100110011001100110010101100110011002')
#     assert decoded == {'unit': 20, 'id': 2, 'state': True}


def test_encode_1() -> None:
    encoded = switch2.encode(id=25, unit=16, state=True)
    assert encoded == "01010101011001100101010101100110011001100101011002"


# def test_encode_2() -> None:
#     encoded = switch2.encode(message={'unit': 0, 'id': 31, 'state': False})
#     elf.assertEqual('01100110011001100110010101010101010101010110010102', encoded)


# def test_encode_3() -> None:
#     encoded = switch2.encode(message={'unit': 20, 'id': 2, 'state': True})
#     elf.assertEqual('01010110010101100110011001100110010101100110011002', encoded)
