# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import logging
import unittest

from rfcontrol.protocols import generic2

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestGeneric2(unittest.TestCase):
    def test_decode_1(self) -> None:
        decoded = generic2.decode(
            "011010101010101001011010101010101010101010010101101001101010100102"
        )
        self.assertDictEqual(
            {
                "id": 123,
                "type": 1,
                "value": 1023,
                "freq": 3,
                "battery": 99,
                "checksum": True,
            },
            decoded,
        )

    def test_decode_2(self) -> None:
        decoded = generic2.decode(
            "010110101010101001011010101010101010101010010101101001101010100102"
        )
        self.assertDictEqual(
            {
                "id": 123,
                "type": 1,
                "value": 1023,
                "freq": 3,
                "battery": 99,
                "checksum": False,
            },
            decoded,
        )
