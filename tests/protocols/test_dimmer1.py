# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import logging
import unittest

from rfcontrol.protocols import dimmer1

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestDimmer1(unittest.TestCase):
    def test_decode_1(self) -> None:
        decoded = dimmer1.decode(
            "0200010001010000010001010000010001000101000100010001000100000101000100010000010001000100010001010001000001000100000001000100010001010001000100010003"
        )
        self.assertDictEqual(
            {
                "id": 9565958,
                "all": False,
                "state": None,
                "unit": 0,
                "dimlevel": 15,
            },
            decoded,
        )

    def test_decode_2(self) -> None:
        decoded = dimmer1.decode(
            "0200010001010000010001010000010001000101000100010001000100000101000100010000010001000100010001010001000001000101000001000100010001010001000100010003"
        )
        self.assertDictEqual(
            {
                "id": 9565958,
                "all": False,
                "state": True,
                "unit": 0,
                "dimlevel": 15,
            },
            decoded,
        )

    def test_encode_1(self) -> None:
        encoded = dimmer1.encode(unit=0, id=9565958, all=False, state=None, dimlevel=15)
        self.assertEqual(
            "0200010001010000010001010000010001000101000100010001000100000101000100010000010001000100010001010001000001000100000001000100010001010001000100010003",
            encoded,
        )

        # 020001000101000001000101000001000100010100010001000100010000010100010001000001000100010001000101000100000100000001000100010001010001000100010003
        # 0200010001010000010001010000010001000101000100010001000100000101000100010000010001000100010001010001000001000100000001000100010001010001000100010003
