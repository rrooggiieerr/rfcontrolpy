"""Contact4 protocol: door/window contact sensor with low-battery flag.

Brands: GS-IWDS07.
"""

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
type = RFControlProtocolTypes.CONTACT
brands = ["GS-IWDS07"]
pulse_lengths = [468, 1364, 14096]
pulse_count = 50


def decode(pulses):
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"10101001100110011001011010100101010101011001100102"``.

    Returns:
        Dict with ``id``, ``state`` and ``lowBattery``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    # Ignore if conversion failed or binary string is too short to contain id + lowBattery + contact
    if binary is None or len(binary) < 24:
        return None

    # Binary is now something like:
    # 111010101001110000001010

    # Now we extract the data from that string.
    # | 11101010100111000000 |       1 |     0 | 10 |
    # | ID                   | Battery | State | ?  |
    # Battery: 1 = OK, 0 = low.
    decoded = {
        "id": int(binary[:20], 2),
        "state": binary[21] == "1",
        "lowBattery": binary[20] != "1",
    }
    logger.debug(decoded)
    return decoded


def encode(id: int, state: bool, low_battery: bool = False):
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID.
        state: Contact state.
        low_battery: True if the battery is low.

    Returns:
        Pulse sequence string.
    """
    encoded = binary2pulses(f"{id:020b}", binary2pulses_mapping)
    encoded += binary2pulses(f"{not low_battery:1b}", binary2pulses_mapping)
    encoded += binary2pulses(f"{state:01b}", binary2pulses_mapping)
    encoded += "1001"
    encoded += "02"
    logger.debug(encoded)
    return encoded
