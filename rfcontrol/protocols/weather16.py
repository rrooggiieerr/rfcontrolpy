"""Weather16 protocol: temperature and humidity sensor."""

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

name = "weather16"
type = RFControlProtocolTypes.WEATHER
brands = ["Ea2 labs Bl999"]
pulse_lengths = [500, 1850, 3900, 9000]
pulse_count = 74


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode raw pulse data into weather sensor readings.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"02020202010202010101020101010201010101010201010101010101010102020102010203"``.

    Returns:
        Dict with ``id``, ``unit``, ``temperature``, ``humidity`` and ``lowBattery``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 32:
        return None

    # Binary is now something like:
    # 111101100010001000001000000000110101

    # Now we extract the data from that string.
    # | 1111 01 10 | 0010 | 0010 0000 1000 | 0000 0011 | 0101      |
    # | ID   UU ID | B??? | Temp.          | Humid.    | checksum  |
    # ID: bits 0-7, LSB first; U: Unit, the channel (01 - 1, 10 - 2, 11 - 3)
    # B: battery, 1 = low
    # Temp.: 12-bit signed, LSB first (divide by 10)
    # Humid.: 8-bit signed, LSB first, + 100
    decoded = {
        "id": int(binary[0:8][::-1], 2),
        "unit": int(binary[4:6], 2),
        "temperature": binary2signed(binary[12:24][::-1]) / 10.0,
        "humidity": binary2signed(binary[24:32][::-1]) + 100,
        "lowBattery": binary[8] != "0",
    }
    logger.debug(decoded)
    return decoded
