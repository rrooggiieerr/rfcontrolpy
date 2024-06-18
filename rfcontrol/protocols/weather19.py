# pylint: disable=duplicate-code
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import logging

from rfcontrol.helpers import pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "0"],  # Binary 0
    ["02", "1"],  # Binary 1
    ["03", ""],  # Footer
]

name = "weather19"
type = RFControlProtocolTypes.WEATHER
brands = ["Landmann BBQ Thermometer"]
pulse_lengths = [548, 1008, 1996, 3936]
pulse_count = 66


def decode(pulses):
    # Pulses is something like:
    # 020202010101010101010101010101020101010102010201020101010201020203

    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None:
        return None

    # Binary is now something like:
    # 11100000000000010000101010001011

    # Now we extract the data from that string.
    # 1110 0000 0000 0001 0000 1010 1000 1011
    # IIII IIUU TTTT TTTT TTTT TTTT xxxx xxxx
    # 0    4    8    12   16   20   24   28
    # I: Device ID, 6-bit unsigned Int
    # U: Unit (2 bits + 1, 00=1, 01=2, 10=3)
    # T: Temperature Value, 16-bit signed Int (divide decimal by 10)
    # x: Unused
    sign = -1 if binary[8] == "1" else 1
    decoded = {
        "id": int(binary[:6], 2),
        "unit": int(binary[6:8], 2) + 1,
        "temperature": sign * int(binary[9:24], 2) / 10,
    }
    logger.debug(decoded)
    return decoded
