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

    def test_decode_2(self) -> None:
        decoded = weather13.decode(
            "02010201010201010101010101010101020101020201020102020202010201010202010203"
        )
        self.assertDictEqual({"id": 164, "unit": 1, "temperature": 15.4, "humidity": 77, "lowBattery": False}, decoded)

        
    def test_decode_3(self) -> None:
        decoded = weather13.decode(
            "02010201010201010101010101010101010201020201020102020202010201020101010103"
        )
        self.assertDictEqual({"id": 164, "unit": 1, "temperature": 9.0, "humidity": 80, "lowBattery": False}, decoded)
        
    def test_decode_4(self) -> None:
        decoded = weather13.decode(
            "02020202010101020201020101010101020202010202010202020202010102020101010103"
        )
        self.assertDictEqual({"id": 241, "unit": 3, "temperature": 23.70, "humidity": 48, "lowBattery": True}, decoded)
