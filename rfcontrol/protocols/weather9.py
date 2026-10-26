"""Weather9 protocol: temperature and humidity sensor."""

import logging
from typing import Any

from rfcontrol.helpers import pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "0"],  # Binary 0
    ["02", "1"],  # Binary 1
    ["03", ""],  # Footer
]

name = "weather9"
type = RFControlProtocolTypes.WEATHER
brands = ["TCM"]
pulse_lengths = [412, 2075, 4115, 8070]
pulse_count = 86


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode raw pulse data into weather sensor readings.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes.

    Returns:
        Dict with ``id``, ``unit``, ``temperature``, ``humidity``, ``lowBattery`` and ``sync``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 36:
        return None

    # Now we extract the data from that string.
    # The temperature is sent in °F with an offset of 90 °F, as three nibbles
    # in reverse order (bits 22-25, 18-21 and 14-17). The humidity is two
    # nibbles in reverse order (bits 30-33 and 26-29). Unit is the channel
    # (bits 12-13, 2 bits + 1).
    # Bit 34 is the battery flag and bit 35 the sync flag.

    t0 = int(binary[22:26], 2)
    t1 = int(binary[18:22], 2)
    t2 = int(binary[14:18], 2)
    # (°F * 10 - 1220) / 1.8 gives °C * 10, rounded like the original.
    temperature = round(((t0 * 256 + t1 * 16 + t2) * 10 - 12200) / 18) / 10
    h0 = int(binary[30:34], 2)
    h1 = int(binary[26:30], 2)
    decoded = {
        "id": int(binary[0:8], 2),
        "unit": int(binary[12:14], 2) + 1,
        "temperature": temperature,
        "humidity": h0 * 16 + h1,
        "lowBattery": binary[34] == "1",
        "sync": binary[35] == "1",
    }
    logger.debug(decoded)
    return decoded
