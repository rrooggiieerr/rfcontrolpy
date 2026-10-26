"""Weather15 protocol: temperature and humidity sensor."""

from typing import Any

from rfcontrol.helpers import binary2signed, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "0"],  # Binary 0
    ["02", "1"],  # Binary 1
    ["03", ""],  # Footer
]

name = "weather15"
type = RFControlProtocolTypes.WEATHER
brands = ["Globaltronics GT-WT-01 variant", "Freetec PT-250"]
pulse_lengths = [496, 2048, 4068, 8960]
pulse_count = 76


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode raw pulse data into weather sensor readings.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"0201010202010202010101010101010101020202010201010202010202020102020201010103"``.

    Returns:
        Dict with ``id``, ``unit``, ``temperature``, ``humidity`` and ``lowBattery``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 36:
        return None

    # Binary is now something like:
    # 1001101100000000011101001101110111000

    # Now we extract the data from that string.
    # 1001 1001 0000 0100 0000 1010 0000 0011 1010 1
    # IIII IIII IIII BxUU TTTT TTTT TTTT HHHH HHHH
    # I: 12 bit ID
    # B: 0 full battery; 1 low battery
    # U: Unit, the channel (2 bits + 1, 00=1, 01=2, 10=3)
    # T: 12 bit Temperature: 0000 1001 0001 -> 145 -> 14.5
    # H: 8 bit Humidity
    return {
        "id": int(binary[0:12], 2),
        "unit": int(binary[14:16], 2) + 1,
        "temperature": binary2signed(binary[16:28]) / 10,
        "humidity": int(binary[28:36], 2),
        "lowBattery": binary[12] == "1",
    }
