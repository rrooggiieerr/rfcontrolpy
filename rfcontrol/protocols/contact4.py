# pylint: disable=duplicate-code
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long

import logging

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["10", "1"],  # Binary 1
    ["01", "0"],  # Binary 0
    ["02", ""],
]

# Mapping for encoding.
binary2pulses_mapping = {
    "1": "10",
    "0": "01",
}

name = "contact4"
type = RFControlProtocolTypes.CONTACT
brands = ["GS-IWDS07"]
pulse_lengths = [468, 1364, 14096]
pulse_count = 50


def decode(pulses):
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None:
        return None

    decoded = {
        "id": int(binary[:20], 2),
        "state": binary[21] == "1",
        "low_battery": int(binary[20], 2) != 1
    }
    logger.debug(decoded)
    return decoded


def encode(id: int, state: bool, low_battery: bool = False):
    encoded = binary2pulses(f"{id:020b}", binary2pulses_mapping)
    encoded += binary2pulses(f"{state:01b}", binary2pulses_mapping)
    encoded += "02"
    logger.debug(encoded)
    return encoded
