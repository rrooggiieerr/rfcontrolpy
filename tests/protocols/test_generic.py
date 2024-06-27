# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import logging
import unittest

from rfcontrol.protocols import generic

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestGeneric(unittest.TestCase):
    def test_decode_1(self) -> None:
        decoded = generic.decode(
            "020102010201020101020102010201020102020101020201020102010102020101020201010202010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201010203"
        )
        self.assertDictEqual(
            {"id": 1000, "type": 10, "positive": True, "value": 1}, decoded
        )

    def test_decode_2(self) -> None:
        decoded = generic.decode(
            "020102010201020101020102010201020102020101020201020102010102020101020201010202010201020102010201020102010201020102010201020102010201020102010201020102010102020102010102010201020201010202010201010203"
        )
        self.assertDictEqual(
            {"id": 1000, "type": 10, "positive": True, "value": 1257}, decoded
        )

    def test_decode_3(self) -> None:
        decoded = generic.decode(
            "020102010201020101020102010201020102010202010201010201020102020101020201010202010201020102010201020102010201020102010201020102010102020102010201020102010102010202010201020101020102010202010201010203"
        )
        self.assertDictEqual(
            {"id": 1011, "type": 10, "positive": True, "value": 67129}, decoded
        )

    def test_decode_4(self) -> None:
        decoded = generic.decode(
            "020102010201020101020102010201020102020101020201020102010102020101020201020102010201020102010201020102010201020102010201020102010102020102010201020102010102010202010201020101020102010202010201010203"
        )
        self.assertDictEqual(
            {"id": 1000, "type": 10, "positive": False, "value": 67129}, decoded
        )

    def test_decode_5(self) -> None:
        decoded = generic.decode(
            "020102010201020101020102010201020102020101020201020102010102020101020201010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010201020102010203"
        )
        self.assertDictEqual(
            {"id": 1000, "type": 10, "positive": True, "value": 1073741823}, decoded
        )
