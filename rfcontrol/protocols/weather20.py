"""Weather20 protocol: temperature sensor."""

import logging
from typing import Any

from rfcontrol.helpers import binary2signed, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "0"],  # Binary 0
    ["02", "0"],  # Binary 0
    ["03", "1"],  # Binary 1
    ["04", ""],  # Footer
]

name = "weather20"
type = RFControlProtocolTypes.WEATHER
brands = ["Freetec PT-250 variant"]
pulse_lengths = [560, 972, 1904, 3812, 8556]
pulse_count = 76


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode raw pulse data into weather sensor readings.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"0302020302020202030202020302020202020202030302020202030202020202020202020104"``.

    Returns:
        Dict with ``id``, ``unit``, ``temperature`` and ``lowBattery``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None or len(binary) < 28:
        return None

    # Binary is now something like:
    # 1001000010001000000011000010000000000

    # Now we extract the data from that string.
    # 1001 1001 0000 0100 0000 1010 0000 0011 1010 1
    # IIII IIII IIII BxUU TTTT TTTT TTTT HHHH HHHH
    # I: 12 bit ID
    # B: 0 full battery; 1 low battery
    # U: Unit, the channel (2 bits + 1, 00=1, 01=2, 10=3)
    # T: 12 bit Temperature: 0000 1001 0001 -> 145 -> 14.5
    # H: 8 bit Humidity
    # The humidity isn't used.
    decoded = {
        "id": int(binary[0:12], 2),
        "unit": int(binary[14:16], 2) + 1,
        "temperature": binary2signed(binary[16:28]) / 10,
        "lowBattery": binary[12] == "1",
    }
    logger.debug(decoded)
    return decoded
