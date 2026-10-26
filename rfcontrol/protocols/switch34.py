"""Switch34 protocol: switches (experimental).

Brands: conecto SA-CC50132.

This protocol was never finished in the original implementation: decoding
also returns the raw bits and bytes, ``state`` is always True, and encoding
always sends the same fixed code. Its own test in the original implementation
fails.
"""

import logging
from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

logger = logging.getLogger(__name__)

# Mapping for decoding.
pulses2binary_mapping = [
    ["11", "0"],  # Binary 0
    ["10", "0"],  # Binary 0
    ["01", "1"],  # Binary 1
    ["00", "1"],  # Binary 1
    ["2", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "11", "1": "01"}

name = "switch34"
type = RFControlProtocolTypes.SWITCH
brands = ["conecto SA-CC50132"]
pulse_lengths = [316, 844, 10360]
pulse_count = 68


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"01010101101010011001010101011010010101011010101010010101011001010102"``.

    Returns:
        Dict with ``bits``, ``bytes``, ``id``, ``unit``, ``all`` and
        ``state``; ``state`` is always True, or None if the pulses don't
        match the protocol.
    """
    # The first pulse is a header and is skipped.
    # We first map the sequences to binary.
    binary = pulses2binary(pulses[1:], pulses2binary_mapping)

    if binary is None or len(binary) < 33:
        return None

    decoded = {
        "bits": binary,
        "bytes": [
            int(binary[offset : offset + 8], 2)
            for offset in range(0, min(len(binary), 32), 8)
        ],
        "id": int(binary[0:17], 2),
        # Like the original implementation, the missing fourth bit is read as 0.
        "unit": int(binary[30:34].ljust(4, "0"), 2),
        "all": binary[14] == "1",
        "state": True,
    }
    logger.debug(decoded)
    return decoded


def encode(id: int = 0, unit: int = 0, state: bool = True, all: bool = False) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Ignored, a fixed code is sent.
        unit: Ignored, a fixed code is sent.
        state: Ignored, a fixed code is sent.
        all: Ignored, a fixed code is sent.

    Returns:
        Pulse sequence string.
    """
    encoded = "0"
    encoded += binary2pulses("000011101000001100001111100001000", binary2pulses_mapping)
    encoded += "2"
    logger.debug(encoded)
    return encoded
