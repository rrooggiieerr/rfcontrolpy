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
    ["02", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {
    "0": "01",
    "1": "10",
}

name = "contact4"
type = "contact"  # RFControlProtocolTypes does not have a CONTACT type yet
brands = ["GS-IWDS07"]
pulse_lengths = [468, 1364, 14096]
pulse_count = 50


def decode(pulses):
    binary = pulses2binary(pulses, pulses2binary_mapping)

    # Ignore if conversion failed or binary string is too short to contain id + lowBattery + contact
    if binary is None or len(binary) < 22:
        return None

    decoded = {
        "id": int(binary[0:20], 2),
        "state": binary[21] != "1",
        "lowBattery": binary[20] != "1",
    }
    logger.debug(decoded)
    return decoded


def encode(id: int, state: bool, lowBattery: bool):
    encoded = ""
    encoded += binary2pulses(f"{id:020b}", binary2pulses_mapping)
    encoded += binary2pulses_mapping["0"] if lowBattery else binary2pulses_mapping["1"]
    encoded += binary2pulses_mapping["1"] if state else binary2pulses_mapping["0"]
    encoded += "02"
    logger.debug(encoded)
    return encoded
