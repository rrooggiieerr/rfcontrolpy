import logging
import unittest

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

import rfcontrol.protocols.switch4 as switch4


class TestSwitch4(unittest.TestCase):
    def test_decode_1(self) -> None:
        decoded = switch4.decode("01010101010101010101011001100110011001100110011002")
        self.assertDictEqual({"unit": 31, "id": 0, "state": True}, decoded)

    def test_decode_2(self) -> None:
        decoded = switch4.decode("01100110011001100110010101010101010101010110010102")
        self.assertDictEqual({"unit": 0, "id": 31, "state": False}, decoded)

    def test_decode_3(self) -> None:
        decoded = switch4.decode("01010110010101100110011001100110010101100110011002")
        self.assertDictEqual({"unit": 20, "id": 2, "state": True}, decoded)

    def test_encode_1(self) -> None:
        encoded = switch4.encode(unit=31, id=0, state=True)
        self.assertEqual("01010101010101010101011001100110011001100110011002", encoded)

    def test_encode_2(self) -> None:
        encoded = switch4.encode(unit=0, id=31, state=False)
        self.assertEqual("01100110011001100110010101010101010101010110010102", encoded)

    def test_encode_3(self) -> None:
        encoded = switch4.encode(unit=20, id=2, state=True)
        self.assertEqual("01010110010101100110011001100110010101100110011002", encoded)
