# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import logging
import unittest

from rfcontrol.protocols import pir1

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestPir1(unittest.TestCase):
    def test_decode_1(self) -> None:
        decoded = pir1.decode("01100101011001100110011001100110011001010110011002")
        self.assertDictEqual({"id": 1, "unit": 8, "state": True}, decoded)

    def test_decode_2(self) -> None:
        decoded = pir1.decode("01100110011001100110010101100110011001010110011002")
        self.assertDictEqual({"id": 17, "unit": 0, "state": True}, decoded)

    def test_decode_3(self) -> None:
        decoded = pir1.decode("01100110011001010110011001100110010101100110011002")
        self.assertDictEqual({"id": 2, "unit": 2, "state": True}, decoded)
