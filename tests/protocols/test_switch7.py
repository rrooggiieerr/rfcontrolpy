# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import logging
import unittest

from rfcontrol.protocols import switch7

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestSwitch7(unittest.TestCase):
    def test_decode_1(self) -> None:
        decoded = switch7.decode("01010101010101100110011001100110011001100110011002")
        self.assertDictEqual({"id": 0, "unit": 3, "state": True}, decoded)

    def test_decode_2(self) -> None:
        decoded = switch7.decode("01010101010101100101010101010110011001100110011002")
        self.assertDictEqual({"id": 7, "unit": 3, "state": True}, decoded)

    def test_decode_3(self) -> None:
        decoded = switch7.decode("10100101011001100101010101010110011001100110011002")
        self.assertDictEqual({"id": 7, "unit": 1, "state": False}, decoded)

    def test_encode_1(self) -> None:
        encoded = switch7.encode(id=0, unit=3, state=True)
        self.assertEqual(
            "01010101010101100110011001100110011001100110011002",
            encoded,
        )

    def test_encode_2(self) -> None:
        encoded = switch7.encode(id=7, unit=3, state=True)
        self.assertEqual(
            "01010101010101100101010101010110011001100110011002",
            encoded,
        )

    def test_encode_3(self) -> None:
        encoded = switch7.encode(id=7, unit=1, state=False)
        self.assertEqual(
            "10100101011001100101010101010110011001100110011002",
            encoded,
        )
