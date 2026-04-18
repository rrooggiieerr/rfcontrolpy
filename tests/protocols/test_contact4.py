# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import logging
import unittest

from rfcontrol.protocols import contact4

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class TestContact4(unittest.TestCase):
    def test_decode_open_1(self) -> None:
        decoded = contact4.decode("01101001100110100101100101010110101010100110011012")
        self.assertDictEqual({"id": 609760, "contact": True, "lowBattery": False}, decoded)

    def test_decode_close_1(self) -> None:
        decoded = contact4.decode("01101001100110100101100101010110101010100101011012")
        self.assertDictEqual({"id": 609760, "contact": False, "lowBattery": False}, decoded)

if __name__ == "__main__":
    unittest.main()
    
