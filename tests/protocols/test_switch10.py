import logging
import unittest

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

import rfcontrol.protocols.switch10 as switch10


class TestSwitch10(unittest.TestCase):
    def test_decode_1(self) -> None:
        decoded = switch10.decode(
            "01010000000101010100000100010101010000000101010100000101000100000101000101010001000100010001010001000101000000010102"
        )
        self.assertDictEqual(
            {"id": 3162089194, "unit": 35, "all": False, "state": False}, decoded
        )

    def test_encode_1(self) -> None:
        encoded = switch10.encode(id=3162089194, unit=35, all=False, state=False)
        self.assertEqual(
            "01010000000101010100000100010101010000000101010100000101000100000101000101010001000100010001010001000101000000010102",
            encoded,
        )
        #  01010000000101010100000100010101010000000101010100000101000100000101000101010001000100010001010100000101000000010102
