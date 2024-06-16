# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import logging
import unittest

from rfcontrol.protocols import switch8

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestSwitch8(unittest.TestCase):
    def test_decode_1(self) -> None:
        decoded = switch8.decode("01010101010101010110011001100110101001011010010102")
        self.assertDictEqual({"id": 30, "unit": "B1", "state": False}, decoded)

    def test_decode_2(self) -> None:
        decoded = switch8.decode("01010101010101010110011001101010010101010101101002")
        self.assertDictEqual({"id": 30, "unit": "C3", "state": True}, decoded)

    def test_decode_3(self) -> None:
        decoded = switch8.decode("01010101010101010101011001101010010101010101101002")
        self.assertDictEqual({"id": 31, "unit": "C3", "state": True}, decoded)

    def test_decode_4(self) -> None:
        decoded = switch8.decode("01100110011001100101011001101010011001010101101002")
        self.assertDictEqual({"id": 1, "unit": "C1", "state": True}, decoded)

    def test_decode_5(self) -> None:
        decoded = switch8.decode("01100110011001100101011001101010010101100101101002")
        self.assertDictEqual({"id": 1, "unit": "C2", "state": True}, decoded)

    def test_encode_1(self) -> None:
        encoded = switch8.encode(id=30, unit="B1", state=False)
        self.assertEqual("01010101010101010110011001100110101001011010010102", encoded)

    def test_encode_2(self) -> None:
        encoded = switch8.encode(id=30, unit="C3", state=True)
        self.assertEqual("01010101010101010110011001101010010101010101101002", encoded)

    def test_encode_3(self) -> None:
        encoded = switch8.encode(id=31, unit="C3", state=True)
        self.assertEqual("01010101010101010101011001101010010101010101101002", encoded)

    def test_encode_4(self) -> None:
        encoded = switch8.encode(id=1, unit="C1", state=True)
        self.assertEqual("01100110011001100101011001101010011001010101101002", encoded)

    def test_encode_5(self) -> None:
        encoded = switch8.encode(id=1, unit="C2", state=True)
        self.assertEqual("01100110011001100101011001101010010101100101101002", encoded)
