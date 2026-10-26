"""Weather8 protocol: temperature and humidity sensor."""

from typing import Any

from rfcontrol.helpers import binary2signed, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "0"],  # Binary 0
    ["02", "1"],  # Binary 1
    ["03", ""],  # Footer
]

name = "weather8"
type = RFControlProtocolTypes.WEATHER
brands: list[str] = []
pulse_lengths = [200, 1000, 2000, 8000]
pulse_count = 74


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode raw pulse data into weather sensor readings.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"01010101020202010202020202020202020201010102010102020202010202020101020103"``.

    Returns:
        Dict with ``id``, ``temperature`` and ``humidity``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 36:
        return None

    # Binary is now something like:
    # 000011101111111111000100111101110010

    # Now we extract the data from that string.
    #   0-----7    8-----15   16----23   24---------35
    # | 00001110 | 11111111 | 11000100 | 111101110010 |
    # | ID       | battery? | Humid.   | Temp.        |
    return {
        "id": int(binary[0:8], 2),
        "temperature": binary2signed(binary[24:36]) / 10.0,
        "humidity": int(binary[16:24], 2),
    }
