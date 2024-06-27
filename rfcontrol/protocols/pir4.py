# pylint: disable=duplicate-code
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import logging

from rfcontrol.helpers import pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["0", "0"],  # Binary 0
    ["1", "1"],  # Binary 1
    ["2", ""],  # Footer
]

# Mapping for encoding
binary2pulses_mapping = {}

name = "pir4"
type = RFControlProtocolTypes.PIR
brands = ["SelectPlus Doorbell"]
pulse_lengths = [371, 1081, 5803]
pulse_count = 36


def decode(pulses):
    # Pulses is something like:
    # 011010011010010110101010010101101010011001100110100101100101101002

    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

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
