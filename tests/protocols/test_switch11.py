# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import logging
import unittest

from rfcontrol.protocols import switch11

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestSwitch11(unittest.TestCase):
    def test_decode_1(self) -> None:
        decoded = switch11.decode(
            "100101010110011010101001101001010101100110010110011010100110011002"
        )
        self.assertDictEqual({"id": 34037, "unit": 1, "state": True}, decoded)

    def test_decode_2(self) -> None:
        decoded = switch11.decode(
            "100101011010011010101001101001010101100110010110011010100110011002"
        )
        self.assertDictEqual({"id": 34037, "unit": 1, "state": False}, decoded)

    def test_decode_3(self) -> None:
        decoded = switch11.decode(
            "100101101001011010101001101001010101100110010110011010100110011002"
        )
        self.assertDictEqual({"id": 34037, "unit": 0, "state": True}, decoded)

    def test_decode_4(self) -> None:
        decoded = switch11.decode(
            "100101100110011010101001101001010101100110010110011010100110011002"
        )
        self.assertDictEqual({"id": 34037, "unit": 0, "state": False}, decoded)

    def test_encode_1(self) -> None:
        encoded = switch11.encode(id=34037, unit=1, state=True)
        self.assertEqual(
            "011010010110011010101001101001010101100110010110011010100110011002",
            encoded,
        )

    def test_encode_2(self) -> None:
        encoded = switch11.encode(id=34037, unit=1, state=False)
        self.assertEqual(
            "011010011010011010101001101001010101100110010110011010100110011002",
            encoded,
        )

    def test_encode_3(self) -> None:
        encoded = switch11.encode(id=34037, unit=0, state=True)
        self.assertEqual(
            "011010101001011010101001101001010101100110010110011010100110011002",
            encoded,
        )

    def test_encode_4(self) -> None:
        encoded = switch11.encode(id=34037, unit=0, state=False)
        self.assertEqual(
            "011010100110011010101001101001010101100110010110011010100110011002",
            encoded,
        )
