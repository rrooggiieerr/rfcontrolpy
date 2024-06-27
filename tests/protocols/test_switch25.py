# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import logging
import unittest

from rfcontrol.protocols import switch25

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestSwitch25(unittest.TestCase):
    def test_decode_1(self) -> None:
        decoded = switch25.decode(
            "101010101010101010101010101010100101010101010101011010100110011002"
        )
        self.assertDictEqual({"id": 0, "unit": 14, "state": True}, decoded)

    def test_decode_2(self) -> None:
        decoded = switch25.decode(
            "101010101010101010101010101010100101010101010101011010100101101002"
        )
        self.assertDictEqual({"id": 0, "unit": 14, "state": False}, decoded)

    def test_decode_3(self) -> None:
        decoded = switch25.decode(
            "101010101010101010101010101010100101010101010101011001101010011002"
        )
        self.assertDictEqual({"id": 0, "unit": 11, "state": True}, decoded)

    def test_decode_4(self) -> None:
        decoded = switch25.decode(
            "101010101010101010101010101010100101010101010101011001101001101002"
        )
        self.assertDictEqual({"id": 0, "unit": 11, "state": False}, decoded)

    def test_decode_5(self) -> None:
        decoded = switch25.decode(
            "101010101010101010101010101010100101010101010101010110101010011002"
        )
        self.assertDictEqual({"id": 0, "unit": 7, "state": True}, decoded)

    def test_decode_6(self) -> None:
        decoded = switch25.decode(
            "101010101010101010101010101010100101010101010101010110101001101002"
        )
        self.assertDictEqual({"id": 0, "unit": 7, "state": False}, decoded)

    def test_decode_7(self) -> None:
        decoded = switch25.decode(
            "101010101010101010101010101010100101010101010101011010011010011002"
        )
        self.assertDictEqual({"id": 0, "unit": 13, "state": True}, decoded)

    def test_decode_8(self) -> None:
        decoded = switch25.decode(
            "101010101010101010101010101010100101010101010101011010011001101002"
        )
        self.assertDictEqual({"id": 0, "unit": 13, "state": False}, decoded)

    def test_decode_9(self) -> None:
        decoded = switch25.decode(
            "101010101010101010101010101010100101010101010101010101010110011002"
        )
        self.assertDictEqual({"id": 0, "unit": 0, "state": True}, decoded)

    def test_decode_10(self) -> None:
        decoded = switch25.decode(
            "101010101010101010101010101010100101010101010101010101010101101002"
        )
        self.assertDictEqual({"id": 0, "unit": 0, "state": False}, decoded)

    def test_encode_1(self) -> None:
        encoded = switch25.encode(id=0, unit=14, state=True)
        self.assertEqual(
            "101010101010101010101010101010100101010101010101011010100110011002",
            encoded,
        )

    def test_encode_2(self) -> None:
        encoded = switch25.encode(id=0, unit=14, state=False)
        self.assertEqual(
            "101010101010101010101010101010100101010101010101011010100101101002",
            encoded,
        )

    def test_encode_3(self) -> None:
        encoded = switch25.encode(id=0, unit=11, state=True)
        self.assertEqual(
            "101010101010101010101010101010100101010101010101011001101010011002",
            encoded,
        )

    def test_encode_4(self) -> None:
        encoded = switch25.encode(id=0, unit=11, state=False)
        self.assertEqual(
            "101010101010101010101010101010100101010101010101011001101001101002",
            encoded,
        )

    def test_encode_5(self) -> None:
        encoded = switch25.encode(id=0, unit=7, state=True)
        self.assertEqual(
            "101010101010101010101010101010100101010101010101010110101010011002",
            encoded,
        )

    def test_encode_6(self) -> None:
        encoded = switch25.encode(id=0, unit=7, state=False)
        self.assertEqual(
            "101010101010101010101010101010100101010101010101010110101001101002",
            encoded,
        )

    def test_encode_7(self) -> None:
        encoded = switch25.encode(id=0, unit=13, state=True)
        self.assertEqual(
            "101010101010101010101010101010100101010101010101011010011010011002",
            encoded,
        )

    def test_encode_8(self) -> None:
        encoded = switch25.encode(id=0, unit=13, state=False)
        self.assertEqual(
            "101010101010101010101010101010100101010101010101011010011001101002",
            encoded,
        )

    def test_encode_9(self) -> None:
        encoded = switch25.encode(id=0, unit=0, state=True)
        self.assertEqual(
            "101010101010101010101010101010100101010101010101010101010110011002",
            encoded,
        )

    def test_encode_10(self) -> None:
        encoded = switch25.encode(id=0, unit=0, state=False)
        self.assertEqual(
            "101010101010101010101010101010100101010101010101010101010101101002",
            encoded,
        )
