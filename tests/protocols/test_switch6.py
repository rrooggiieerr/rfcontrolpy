# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import logging
import unittest

from rfcontrol.protocols import switch6

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestSwitch6(unittest.TestCase):
    def test_decode_1(self) -> None:
        decoded = switch6.decode("10101010101010101010010101100110011001100110010102")
        self.assertDictEqual({"id": 31, "unit": 1, "state": True}, decoded)

    def test_decode_2(self) -> None:
        decoded = switch6.decode("10101010101010100110011001010110011001100110010102")
        self.assertDictEqual({"id": 15, "unit": 2, "state": True}, decoded)

    def test_encode_1(self) -> None:
        encoded = switch6.encode(id=31, unit=1, state=True)
        self.assertEqual(
            "10101010101010101010010101100110011001100110010102",
            encoded,
        )

    def test_encode_2(self) -> None:
        encoded = switch6.encode(id=15, unit=2, state=True)
        self.assertEqual(
            "10101010101010100110011001010110011001100110010102",
            encoded,
        )
