"""Weather6 protocol: temperature and humidity sensor."""

from typing import Any

from rfcontrol.helpers import binary2signed, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "0"],  # Binary 0
    ["02", "1"],  # Binary 1
    ["03", ""],  # Footer
]

name = "weather6"
type = RFControlProtocolTypes.WEATHER
brands = ["Sempre GT-WT-02"]
pulse_lengths = [552, 2089, 4137, 9032]
pulse_count = 80


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode raw pulse data into weather sensor readings.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"01020102010202020101010101010101010201020201020102010102020101020102020101030103"``.

    Returns:
        Dict with ``id``, ``unit``, ``temperature``, ``humidity`` and ``lowBattery``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 38:
        return None

    # Binary is now something like:
    # 01010111000000000101101010011001011000

    # Now we extract the data from that string.
    # | 01010111 | 00   | 00 | 000001011010 | 1001100  | 101100 | 0 |
    # | ID       | Unit | ?  | Temp.        | Humid.   | ?      | B |
    # Unit: channel (2 bits + 1); B: battery, 1 = OK
    return {
        "id": int(binary[0:8], 2),
        "unit": int(binary[8:10], 2) + 1,
        "temperature": binary2signed(binary[12:24]) / 10,
        "humidity": int(binary[24:31], 2),
        "lowBattery": binary[37] != "1",
    }
