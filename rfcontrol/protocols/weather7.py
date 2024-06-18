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

name = "weather7"
type = RFControlProtocolTypes.WEATHER
brands = ["Auriol IAN 9183"]
pulse_lengths = [456, 1990, 3940, 9236]
pulse_count = 66


def decode(pulses):
    # Pulses is something like:
    # 01020102020201020101010101010102010101010202020101020202010102010101020103

    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None:
        return None

    # Binary is now something like:
    # 010111010000000100001110011100100010

    # Now we extract the data from that string.
    #   0-----7     8  14-15   16--------27   28----35
    # | 10001101 | 11 | 000100001001 | 00111101 |
    # |    ID    | BT | Temp.        | Humid.   |
    decoded = {
        "id": int(binary[:8], 2),
        "unit": int(binary[10:12], 2),
        "temperature": int(binary[12:24], 2) / 10,
        "humidity": int(binary[24:30], 2),
        "lowBattery": binary[8] != "1",
    }
    logger.debug(decoded)
    return decoded
