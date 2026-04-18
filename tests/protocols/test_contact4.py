# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import logging
import unittest

from rfcontrol.protocols import contact4

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestContact4(unittest.TestCase):
    def test_decode_open_1(self) -> None:
        decoded = contact4.decode("10010110011001011010011010101001010101011010100102")
        self.assertIsNotNone(decoded)
        self.assertDictEqual(
            {"id": 609760, "state": True, "lowBattery": False}, decoded
        )

    def test_decode_open_2(self) -> None:
        decoded = contact4.decode("10101001100110011001011010100101010101011010100102")
        self.assertIsNotNone(decoded)
        self.assertDictEqual(
            {"id": 960960, "state": True, "lowBattery": False}, decoded
        )

    def test_decode_open_3(self) -> None:
        decoded = contact4.decode("01011010101001010110010110010101010101011010100102")
        self.assertIsNotNone(decoded)
        self.assertDictEqual(
            {"id": 246912, "state": True, "lowBattery": False}, decoded
        )

    def test_decode_close_1(self) -> None:
        decoded = contact4.decode("10010110011001011010011010101001010101011001100102")
        self.assertIsNotNone(decoded)
        self.assertDictEqual(
            {"id": 609760, "state": False, "lowBattery": False}, decoded
        )

    def test_decode_close_2(self) -> None:
        decoded = contact4.decode("10101001100110011001011010100101010101011001100102")
        self.assertIsNotNone(decoded)
        self.assertDictEqual(
            {"id": 960960, "state": False, "lowBattery": False}, decoded
        )

    def test_decode_close_3(self) -> None:
        decoded = contact4.decode("01011010101001010110010110010101010101011001100102")
        self.assertIsNotNone(decoded)
        self.assertDictEqual(
            {"id": 246912, "state": False, "lowBattery": False}, decoded
        )

    def test_decode_open_lowbattery(self) -> None:
        decoded = contact4.decode("10101001100110011001011010100101010101010110100102")
        self.assertIsNotNone(decoded)
        self.assertDictEqual({"id": 960960, "state": True, "lowBattery": True}, decoded)

    def test_encode_open_1(self) -> None:
        encoded = contact4.encode(id=609760, state=True, low_battery=False)
        self.assertEqual("10010110011001011010011010101001010101011010100102", encoded)

    def test_encode_open_2(self) -> None:
        encoded = contact4.encode(id=960960, state=True, low_battery=False)
        self.assertEqual(
            "10101001100110011001011010100101010101011010100102",
            encoded,
        )

    def test_encode_close_1(self) -> None:
        encoded = contact4.encode(id=609760, state=False, low_battery=False)
        self.assertEqual("10010110011001011010011010101001010101011001100102", encoded)

    def test_encode_close_2(self) -> None:
        encoded = contact4.encode(id=960960, state=False, low_battery=False)
        self.assertEqual(
            "10101001100110011001011010100101010101011001100102",
            encoded,
        )

    def test_encode_open_lowbattery(self) -> None:
        encoded = contact4.encode(id=960960, state=True, low_battery=True)
        self.assertEqual(
            "10101001100110011001011010100101010101010110100102",
            encoded,
        )
