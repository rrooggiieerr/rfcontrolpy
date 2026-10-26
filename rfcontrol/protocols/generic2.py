"""Generic2 protocol: homemade sensors with battery level and checksum."""

from typing import Any

from rfcontrol.helpers import hex_checksum, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

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


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"101001101010100110101010100101010101101010101010011010101010101002"``.

    Returns:
        Dict with ``id``, ``type``, ``value``, ``freq``, ``battery`` and
        ``checksum``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 32:
        return None

    # Binary is now something like:
    # 11011110111110000011111101111111

    # Now we extract the data from that string.
    return {
        "id": int(binary[24:32][::-1], 2),
        "type": int(binary[20:24][::-1], 2),
        "value": int(binary[10:20][::-1], 2),
        "freq": int(binary[6:10][::-1], 2),
        "battery": 33 * int(binary[4:6][::-1], 2),
        "checksum": hex_checksum(binary),
    }
