# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import logging
import unittest

from rfcontrol.protocols import weather5

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestWeather5(unittest.TestCase):
    def test_decode_1(self) -> None:
        decoded = weather5.decode(
            "01020101010201020102010101020202020202010101010102020201010202010202020203"
        )
        self.assertDictEqual(
            {
                "id": 162,
                "temperature": 12.6,
                "humidity": 67,
                "lowBattery": False,
            },
            decoded,
        )

    def test_decode_2(self) -> None:
        decoded = weather5.decode(
            "01010101010101010102020102020101020202010201010101010101010101010101010203"
        )
        self.assertDictEqual(
            {
                "id": 0,
                "rain": 5.75,
                "lowBattery": False,
            },
            decoded,
        )

    def test_decode_3(self) -> None:
        decoded = weather5.decode(
            "01020202010101020102020102020101020102020202010101010101010101010102020103"
        )
        self.assertDictEqual(
            {
                "id": 142,
                "rain": 15.25,
                "lowBattery": False,
            },
            decoded,
        )

    def test_decode_4(self) -> None:
        decoded = weather5.decode(
            "01020202010202020101010102010201020202010101010102010102020101020201020103"
        )
        self.assertDictEqual(
            {
                "id": 238,
                "temperature": 11.7,
                "humidity": 99,
                "lowBattery": False,
            },
            decoded,
        )

    def test_decode_5(self) -> None:
        decoded = weather5.decode(
            "01020202010202020101020101020101020202020202020202010102010202010101010103"
        )
        self.assertDictEqual(
            {
                "id": 238,
                "temperature": -1.4,
                "humidity": 69,
                "lowBattery": False,
            },
            decoded,
        )
