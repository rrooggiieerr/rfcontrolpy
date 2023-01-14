import logging
import unittest

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

import rfcontrol.protocols.pir3 as pir3


class TestPir3(unittest.TestCase):
    def test_decode_1(self) -> None:
        decoded = pir3.decode(
            "100110100110011001100110101001101010011001100110100101100101101002"
        )
        self.assertDictEqual({"id": 19106, "unit": 10860, "state": True}, decoded)
