# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import logging
import unittest

from rfcontrol.protocols import switch5

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestSwitch5(unittest.TestCase):
    def test_decode_1(self) -> None:
        decoded = switch5.decode("10010101101010010110010110101001010101011010101002")
        self.assertDictEqual(
            {"id": 465695, "unit": 1, "all": False, "state": True}, decoded
        )

    def test_decode_2(self) -> None:
        decoded = switch5.decode("10010101101010010110010110101001010101011010100102")
        self.assertDictEqual(
            {"id": 465695, "unit": 1, "all": False, "state": False}, decoded
        )

    def test_decode_3(self) -> None:
        decoded = switch5.decode("10010101101010010110010110101001010101011010011002")
        self.assertDictEqual(
            {"id": 465695, "unit": 2, "all": False, "state": True}, decoded
        )

    def test_decode_4(self) -> None:
        decoded = switch5.decode("10010101101010010110010110101001010101011010010102")
        self.assertDictEqual(
            {"id": 465695, "unit": 2, "all": False, "state": False}, decoded
        )

    def test_decode_5(self) -> None:
        decoded = switch5.decode("10010101101010010110010110101001010101011001101002")
        self.assertDictEqual(
            {"id": 465695, "unit": 3, "all": False, "state": True}, decoded
        )

    def test_decode_6(self) -> None:
        decoded = switch5.decode("10010101101010010110010110101001010101011001100102")
        self.assertDictEqual(
            {"id": 465695, "unit": 3, "all": False, "state": False}, decoded
        )

    def test_decode_7(self) -> None:
        decoded = switch5.decode("10010101101010010110010110101001010101010110101002")
        self.assertDictEqual(
            {"id": 465695, "unit": 4, "all": False, "state": True}, decoded
        )

    def test_decode_8(self) -> None:
        decoded = switch5.decode("10010101101010010110010110101001010101010110100102")
        self.assertDictEqual(
            {"id": 465695, "unit": 4, "all": False, "state": False}, decoded
        )

    def test_decode_9(self) -> None:
        decoded = switch5.decode("10010101101010010110010110101001010101010101011002")
        self.assertDictEqual(
            {"id": 465695, "unit": 0, "all": True, "state": False}, decoded
        )

    def test_decode_10(self) -> None:
        decoded = switch5.decode("10010101101010010110010110101001010101010101100102")
        self.assertDictEqual(
            {"id": 465695, "unit": 0, "all": True, "state": True}, decoded
        )

    def test_encode_1(self) -> None:
        encoded = switch5.encode(id=465695, unit=1, all=False, state=True)
        self.assertEqual(
            "10010101101010010110010110101001010101011010101002",
            encoded,
        )

    def test_encode_2(self) -> None:
        encoded = switch5.encode(id=465695, unit=1, all=False, state=False)
        self.assertEqual(
            "10010101101010010110010110101001010101011010100102",
            encoded,
        )

    def test_encode_3(self) -> None:
        encoded = switch5.encode(id=465695, unit=2, all=False, state=True)
        self.assertEqual(
            "10010101101010010110010110101001010101011010011002",
            encoded,
        )

    def test_encode_4(self) -> None:
        encoded = switch5.encode(id=465695, unit=2, all=False, state=False)
        self.assertEqual(
            "10010101101010010110010110101001010101011010010102",
            encoded,
        )

    def test_encode_5(self) -> None:
        encoded = switch5.encode(id=465695, unit=3, all=False, state=True)
        self.assertEqual(
            "10010101101010010110010110101001010101011001101002",
            encoded,
        )

    def test_encode_6(self) -> None:
        encoded = switch5.encode(id=465695, unit=3, all=False, state=False)
        self.assertEqual(
            "10010101101010010110010110101001010101011001100102",
            encoded,
        )

    def test_encode_7(self) -> None:
        encoded = switch5.encode(id=465695, unit=4, all=False, state=True)
        self.assertEqual(
            "10010101101010010110010110101001010101010110101002",
            encoded,
        )

    def test_encode_8(self) -> None:
        encoded = switch5.encode(id=465695, unit=4, all=False, state=False)
        self.assertEqual(
            "10010101101010010110010110101001010101010110100102",
            encoded,
        )

    def test_encode_9(self) -> None:
        encoded = switch5.encode(id=465695, unit=0, all=True, state=False)
        self.assertEqual(
            "10010101101010010110010110101001010101010101011002",
            encoded,
        )

    def test_encode_10(self) -> None:
        encoded = switch5.encode(id=465695, unit=0, all=True, state=True)
        self.assertEqual(
            "10010101101010010110010110101001010101010101100102",
            encoded,
        )
