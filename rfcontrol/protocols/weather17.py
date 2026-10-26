"""Weather17 protocol: temperature or humidity sensor.

Every message carries either the temperature or the humidity.
"""

from typing import Any

from rfcontrol.helpers import pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["11", "0"],  # Binary 0
    ["01", "1"],  # Binary 1
    ["02", ""],  # Footer
    ["12", ""],  # Footer
]

name = "weather17"
type = RFControlProtocolTypes.WEATHER
brands = ["TFA 30.3125"]
pulse_lengths = [444, 1160, 28580]
pulse_count = 88


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode raw pulse data into weather sensor readings.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"1111111101110111111111111111010111111111110101011111111111111101110101011111111101011112"``.

    Returns:
        Dict with ``id`` and either ``temperature`` or ``humidity``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 32:
        return None

    # Binary is now something like:
    # 0000101000000011000001110000000101110000110

    # Now we extract the data from that string.
    # | 8 bits | 3 bits | 1 bit | 7 bits | 1 bit | 4 bits | 4 bits | 4 bits |
    # | ?      | Type   | ?     | ID     | ?     | tens   | ones   | tenths |
    # Type 0 (000) means a temperature message, 7 (111) a humidity message.
    # The original implementation returns the type as ``channel``; it isn't
    # returned here, since the temperature or humidity key already tells it.
    # 5 has to be subtracted from the tens of the temperature.
    # The ID changes when the battery is replaced.
    p0 = int(binary[20:24], 2)
    p1 = int(binary[24:28], 2)
    p2 = int(binary[28:32], 2)
    decoded: dict[str, int | float] = {"id": int(binary[12:19], 2)}
    if int(binary[8:11], 2) == 0:
        decoded["temperature"] = ((p0 - 5) * 10) + p1 + (p2 * 0.1)
    else:
        decoded["humidity"] = p0 * 10 + p1
    return decoded
