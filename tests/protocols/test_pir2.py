# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import logging
import unittest

from rfcontrol.protocols import pir2

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestPir2(unittest.TestCase):
    def test_decode_1(self) -> None:
        decoded = pir2.decode("01100110010110011001010110100101010101011010010102")
        self.assertDictEqual({"id": 21, "unit": 21, "state": True}, decoded)
