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
    def test_decode_1(self) -> None:
        decoded = contact4.decode(
            "10101001100110011001011010100101010101011001100102"
        )
        self.assertDictEqual(
            {"id": 960960, "state": False, "low_battery": False}, decoded
        )

    def test_decode_2(self) -> None:
        decoded = contact4.decode(
            "10101001100110011001011010100101010101011010100102"
        )
        self.assertDictEqual(
            {"id": 960960, "state": True, "low_battery": False}, decoded
        )

    def test_decode_3(self) -> None:
        decoded = contact4.decode(
            "10101001100110011001011010100101010101010110100102"
        )
        self.assertDictEqual(
            {"id": 960960, "state": True, "low_battery": True}, decoded
        )

    def test_decode_4(self) -> None:
        decoded = contact4.decode(
            "01011010101001010110010110010101010101011001100102"
        )
        self.assertDictEqual(
            {"id": 246912, "state": False, "low_battery": False}, decoded
        )

    def test_decode_5(self) -> None:
        decoded = contact4.decode(
            "01011010101001010110010110010101010101011010100102"
        )
        self.assertDictEqual(
            {"id": 246912, "state": True, "low_battery": False}, decoded
        )

    # def test_decode_6(self) -> None:
    #     decoded = contact4.decode(
    #         "01011010101001010110010110010101010101010110101002"
    #     )
    #     self.assertDictEqual(
    #         {"id": 246912, "state": False, "low_battery": False}, decoded
    #     )
    #
    # def test_decode_7(self) -> None:
    #     decoded = contact4.decode(
    #         "01011010101001010110010110010101010101011001100102"
    #     )
    #     self.assertDictEqual(
    #         {"id": 246912, "state": True, "low_battery": False}, decoded
    #     )

    def test_encode_1(self) -> None:
        encoded = contact4.encode(id=960960, state=False, low_battery=False)
        self.assertEqual(
            "10101001100110011001011010100101010101011001100102",
            encoded,
        )

    def test_encode_2(self) -> None:
        encoded = contact4.encode(id=960960, state=True, low_battery=False)
        self.assertEqual(
            "10101001100110011001011010100101010101011010100102",
            encoded,
        )

    def test_encode_3(self) -> None:
        encoded = contact4.encode(id=960960, state=True, low_battery=True)
        self.assertEqual(
            "10101001100110011001011010100101010101010110100102",
            encoded,
        )
