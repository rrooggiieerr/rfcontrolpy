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
    ["10", "1"],  # Binary 1
    ["02", ""],  # Footer
]

# Mapping for encoding
binary2pulses_mapping = {}

name = "pir6"
type = RFControlProtocolTypes.PIR
brands = ["Zanbo (ZABC86-1)", "Unknown (OSW-1-3 and OTW-1-3)"]
pulse_lengths = [288, 864, 8964]
pulse_count = 50


def decode(pulses):
    # Pulses is something like:
    #

    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None:
        return None

    # Binary is now something like:
    # 001100001110100011000011

    # Now we extract the data from that string.
    decoded = {
        "id": int(binary[2:25], 2),
        "state": True,
    }
    logger.debug(decoded)
    return decoded
