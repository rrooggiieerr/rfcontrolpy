# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import logging
import unittest

from rfcontrol.protocols import weather19

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestWeather19(unittest.TestCase):
    def test_decode_1(self) -> None:
        decoded = weather19.decode(
            "020202010101010101010101010101020101010102010201020101010201020203"
        )
        self.assertDictEqual({"id": 56, "unit": 1, "temperature": 26.6}, decoded)

    def test_decode_2(self) -> None:
        decoded = weather19.decode(
            "020102020102010101010101010101020101020101020201010102020201020203"
        )
        self.assertDictEqual({"id": 45, "unit": 1, "temperature": 29.4}, decoded)

    def test_decode_3(self) -> None:
        decoded = weather19.decode(
            "020102020102010101010101010101020101020201010101020102010102010203"
        )
        self.assertDictEqual({"id": 45, "unit": 1, "temperature": 30.4}, decoded)

    def test_decode_4(self) -> None:
        decoded = weather19.decode(
            "020102020102010101010101010101020202010102020101020102010101010203"
        )
        self.assertDictEqual({"id": 45, "unit": 1, "temperature": 46.0}, decoded)
