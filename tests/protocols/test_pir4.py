# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import logging
import unittest

from rfcontrol.protocols import pir4

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestPir4(unittest.TestCase):
    def test_decode_1(self) -> None:
        decoded = pir4.decode("110100110101001101010011001010101012")
        self.assertDictEqual({"id": 54099, "unit": 21290, "state": True}, decoded)
