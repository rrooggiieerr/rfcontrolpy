# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import logging
import unittest

from rfcontrol.protocols import weather13

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestWeather13(unittest.TestCase):
    def test_decode_1(self) -> None:
        decoded = weather13.decode(
            "01020102020102020202020202020202010202010102010201010101020102020101020103"
        )
        self.assertDictEqual({"id": 164, "unit": 1, "temperature": 15.4, "humidity": 77, "lowBattery": False}, decoded)
