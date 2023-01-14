import logging
import unittest

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

import rfcontrol.protocols.switch1 as switch1


class TestSwitch1(unittest.TestCase):
    def test_decode_1(self) -> None:
        decoded = switch1.decode(
            "020100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010000010100000100010001000103"
        )
        assert decoded == {"id": 67108863, "all": False, "state": True, "unit": 0}

    def test_decode_2(self) -> None:
        decoded = switch1.decode(
            "020001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000101000001010001000100010003"
        )
        self.assertDictEqual(
            {"id": 0, "all": True, "state": False, "unit": 15}, decoded
        )

    def test_decode_3(self) -> None:
        decoded = switch1.decode(
            "020001000101000001000100010100010001000100000101000001000101000001000100010100000100010100010000010100000100010100000100010001000103"
        )
        self.assertDictEqual(
            {"id": 9390234, "all": False, "state": True, "unit": 0}, decoded
        )

    def test_decode_4(self) -> None:
        decoded = switch1.decode(
            "020001000101000001000100010100010001000100000101000001000101000001000100010100000100010100010000010100000100010100000100010001010003"
        )
        self.assertDictEqual(
            {"id": 9390234, "all": False, "state": True, "unit": 1}, decoded
        )

    def test_decode_5(self) -> None:
        decoded = switch1.decode(
            "020001000101000001000100010100010001000100000101000001000101000001000100010100000100010100010000010100000100010001000100010001010003"
        )
        self.assertDictEqual(
            {"id": 9390234, "all": False, "state": False, "unit": 1}, decoded
        )

    def test_encode_1(self) -> None:
        encoded = switch1.encode(id=67108863, all=False, state=True, unit=0)
        self.assertEqual(
            "020100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010000010100000100010001000103",
            encoded,
        )

    def test_encode_2(self) -> None:
        encoded = switch1.encode(id=0, all=True, state=False, unit=15)
        self.assertEqual(
            "020001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000100010001000101000001010001000100010003",
            encoded,
        )

    def test_encode_3(self) -> None:
        encoded = switch1.encode(id=9390234, all=False, state=True, unit=0)
        self.assertEqual(
            "020001000101000001000100010100010001000100000101000001000101000001000100010100000100010100010000010100000100010100000100010001000103",
            encoded,
        )

    def test_encode_4(self) -> None:
        encoded = switch1.encode(id=9390234, all=False, state=True, unit=1)
        self.assertEqual(
            "020001000101000001000100010100010001000100000101000001000101000001000100010100000100010100010000010100000100010100000100010001010003",
            encoded,
        )

    def test_encode_5(self) -> None:
        encoded = switch1.encode(id=9390234, all=False, state=False, unit=1)
        self.assertEqual(
            "020001000101000001000100010100010001000100000101000001000101000001000100010100000100010100010000010100000100010001000100010001010003",
            encoded,
        )
