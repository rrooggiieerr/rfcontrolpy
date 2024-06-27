# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import logging
import unittest

from rfcontrol.protocols import pir6

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestPir6(unittest.TestCase):
    def test_decode_1(self) -> None:
        decoded = pir6.decode("01011010010101011010100110010101101001010101101002")
        self.assertDictEqual({"id": 6410630, "state": True}, decoded)

    def test_decode_2(self) -> None:
        decoded = pir6.decode("01011010010101011010100110010101101001010110010102")
        self.assertDictEqual({"id": 6410632, "state": True}, decoded)

    def test_decode_3(self) -> None:
        decoded = pir6.decode("01011010010101011010100110010101101001011001010102")
        self.assertDictEqual({"id": 6410640, "state": True}, decoded)
