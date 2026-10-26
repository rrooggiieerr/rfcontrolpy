"""Weather2 protocol: temperature sensor."""

from typing import Any

from rfcontrol.helpers import binary2signed, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "0"],  # Binary 0
    ["02", "1"],  # Binary 1
    ["03", ""],  # Footer
]

name = "weather2"
type = RFControlProtocolTypes.WEATHER
brands = ["Auriol", "Pollin (EWS-151)"]
pulse_lengths = [492, 969, 1948, 4004]
pulse_count = 74


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode raw pulse data into weather sensor readings.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"01010102020202010201010101010101020202010201020102020202010101010101010103"``.

    Returns:
        Dict with ``temperature``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 24:
        return None

    # Binary is now something like:
    # 000111101000000011101010111100000000

    # Now we extract the data from that string.
    # | 000111101000 | 000011101010 | 111100000000 |
    # | ?            | Temp.        | ?            |
    return {
        "temperature": binary2signed(binary[12:24]) / 10,
    }
