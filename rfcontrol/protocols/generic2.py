# pylint: disable=duplicate-code
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import logging

from rfcontrol.helpers import hex_checksum, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "0"],  # Binary 0
    ["10", "1"],  # Binary 1
    ["02", ""],  # Footer
]

name = "generic2"
type = RFControlProtocolTypes.GENERIC
brands = ["homemade"]
pulse_lengths = [480, 1320, 13320]
pulse_count = 66


def decode(pulses):
    # Pulses could be:
    # 101001101010100110101010100101010101101010101010011010101010101002

    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None:
        return None

    # Binary is now something like:
    # 11011110111110000011111101111111

    # Now we extract the data from that string.
    decoded = {
        "id": int(binary[24:32][::-1], 2),
        "type": int(binary[20:23][::-1], 2),
        "value": int(binary[10:20][::-1], 2),
        "freq": int(binary[6:10][::-1], 2),
        "battery": 33 * int(binary[4:6][::-1], 2),
        "checksum": hex_checksum(binary),
    }
    logger.debug(decoded)
    return decoded
