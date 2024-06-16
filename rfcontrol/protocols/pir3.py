# pylint: disable=duplicate-code
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import logging

from rfcontrol.helpers import pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["10", "0"],  # Binary 0
    ["01", "1"],  # Binary 1
    ["02", ""],  # Footer
]

# Mapping for encoding
binary2pulses_mapping = {}

name = "pir3"
type = RFControlProtocolTypes.PIR
brands = ["Inter-Union"]
pulse_lengths = [496, 1471, 6924]
pulse_count = 66


def decode(pulses):
    # Pulses is something like:
    # 011010011010010110101010010101101010011001100110100101100101101002

    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None:
        return None

    # Binary is now something like:
    # 10010011000011100010101001101100

    # Now we extract the data from that string.
    decoded = {
        "id": int(binary[0:16], 2),
        "unit": int(binary[16:32], 2),
        "state": True,
    }
    logger.debug(decoded)
    return decoded
