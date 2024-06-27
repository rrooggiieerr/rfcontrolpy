# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import logging
import unittest

from rfcontrol.protocols import weather7

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestWeather7(unittest.TestCase):
    def test_decode_1(self) -> None:
        decoded = weather7.decode(
            "010202010201010202010101010101010101010202020102020202010202010103"
        )
        self.assertDictEqual(
            {
                "id": 105,
                "unit": 0,
                "temperature": 2.9,
                "humidity": 59,
                "lowBattery": False,
            },
            decoded,
        )
