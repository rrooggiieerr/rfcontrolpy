"""Weather3 protocol: temperature and humidity sensor."""

from typing import Any

from rfcontrol.helpers import pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "0"],  # Binary 0
    ["02", "1"],  # Binary 1
    ["03", ""],  # Footer
]

name = "weather3"
type = RFControlProtocolTypes.WEATHER
brands = ["TFA", "Conrad Electronic"]
pulse_lengths = [508, 2012, 3908, 7726]
pulse_count = 86


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode raw pulse data into weather sensor readings.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"02020101010102010102020201020101020202010102020101020202010102010202020102020201010103"``.

    Returns:
        Dict with ``id``, ``unit``, ``temperature`` and ``humidity``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 34:
        return None

    # Binary is now something like:
    # 110000100111010011100110011100101110111000

    # Now we extract the data from that string.
    # The temperature is sent in °F with an offset of 90 °F, as three nibbles
    # in reverse order (bits 22-25, 18-21 and 14-17). The humidity is two
    # nibbles in reverse order (bits 30-33 and 26-29). Unit is the channel
    # (bits 12-13, 2 bits + 1).

    t0 = int(binary[22:26], 2)
    t1 = int(binary[18:22], 2)
    t2 = int(binary[14:18], 2)
    # (°F * 10 - 1220) / 1.8 gives °C * 10, rounded like the original.
    temperature = round(((t0 * 256 + t1 * 16 + t2) * 10 - 12200) / 18) / 10
    h0 = int(binary[30:34], 2)
    h1 = int(binary[26:30], 2)
    return {
        "id": int(binary[2:10], 2),
        "unit": int(binary[12:14], 2) + 1,
        "temperature": temperature,
        "humidity": h0 * 16 + h1,
    }
