"""Weather1 protocol: temperature and humidity sensor."""

import logging
from typing import Any

from rfcontrol.helpers import binary2signed, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "0"],  # Binary 0
    ["02", "1"],  # Binary 1
    ["03", ""],  # Footer
]

name = "weather1"
type = RFControlProtocolTypes.WEATHER
brands = ["Logilink WS0002", "DANIU"]
pulse_lengths = [456, 1990, 3940, 9236]
pulse_count = 74


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode raw pulse data into weather sensor readings.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"01020102020201020101010101010102010101010202020101020202010102010101020103"``.

    Returns:
        Dict with ``id``, ``unit``, ``temperature``, ``humidity`` and ``lowBattery``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 36:
        return None

    # Binary is now something like:
    # 010111010000000100001110011100100010

    # Now we extract the data from that string.
    #   0--3   4-----11  12-13  14-15   16--------27   28----35
    # | 0101 | 11010000 | 00  |  01  | 000011100111 | 00100010 |
    # | ?    | ID       | BT  | Unit | Temp.        | Humid.   |
    # B: battery, 1 = OK; Unit: channel (2 bits + 1)
    decoded = {
        "id": int(binary[4:12], 2),
        "unit": int(binary[14:16], 2) + 1,
        "temperature": binary2signed(binary[16:28]) / 10,
        "humidity": int(binary[28:36], 2),
        "lowBattery": binary[12] != "1",
    }
    logger.debug(decoded)
    return decoded
