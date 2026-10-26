"""Weather19 protocol: Landmann BBQ thermometer."""

from typing import Any

from rfcontrol.helpers import binary2signed, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "0"],  # Binary 0
    ["02", "1"],  # Binary 1
    ["03", ""],  # Footer
]

name = "weather19"
type = RFControlProtocolTypes.WEATHER
brands = ["Landmann BBQ Thermometer"]
pulse_lengths = [548, 1008, 1996, 3936]
pulse_count = 66


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode raw pulse data into weather sensor readings.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"020202010101010101010101010101020101010102010201020101010201020203"``.

    Returns:
        Dict with ``id``, ``unit`` and ``temperature``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 24:
        return None

    # Binary is now something like:
    # 11100000000000010000101010001011

    # Now we extract the data from that string.
    # 1110 0000 0000 0001 0000 1010 1000 1011
    # IIII IIUU TTTT TTTT TTTT TTTT xxxx xxxx
    # 0    4    8    12   16   20   24   28
    # I: Device ID, 6-bit unsigned Int
    # U: Unit (2 bits + 1, 00=1, 01=2, 10=3)
    # T: Temperature Value, 16-bit signed Int (divide decimal by 10)
    # x: Unused
    return {
        "id": int(binary[:6], 2),
        "unit": int(binary[6:8], 2) + 1,
        "temperature": binary2signed(binary[8:24]) / 10,
    }
