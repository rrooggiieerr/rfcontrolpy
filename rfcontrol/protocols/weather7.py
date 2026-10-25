"""Weather7 protocol: Auriol IAN 9183 temperature and humidity sensor."""

import logging
from typing import Any

from rfcontrol.helpers import binary2signed, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "0"],  # Binary 0
    ["02", "1"],  # Binary 1
    ["03", ""],  # Footer
]

name = "weather7"
type = RFControlProtocolTypes.WEATHER
brands = ["Auriol IAN 9183"]
pulse_lengths = [456, 1990, 3940, 9236]
pulse_count = 66


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode raw pulse data into weather sensor readings.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"010202010201010202010101010101010101010202020102020202010202010103"``.

    Returns:
        Dict with ``id``, ``unit``, ``temperature``, ``humidity`` and
        ``lowBattery``, or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None:
        return None

    # Binary is now something like:
    # 01101001100000000001110111101100

    # Now we extract the data from that string.
    #   0------7   8   9   10-11   12--------23   24---29   30-31
    # | 01101001 | 1 | 0 | 00    | 000000011101 | 111011 | 00 |
    # | ID       | B | ? | Unit  | Temp.        | Humid. | ?  |
    # B: battery, 1 = OK
    decoded = {
        "id": int(binary[:8], 2),
        "unit": int(binary[10:12], 2),
        "temperature": binary2signed(binary[12:24]) / 10,
        "humidity": int(binary[24:30], 2),
        "lowBattery": binary[8] != "1",
    }
    logger.debug(decoded)
    return decoded
