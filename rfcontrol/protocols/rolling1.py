"""Rolling1 protocol: rolling code switches.

Brands: rollingCode.

The decoded code changes with every button press, so a switch is taught by
recording one or more codes for on and off.
"""

from typing import Any

from rfcontrol.helpers import binary2pulses, pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping = [
    ["01", "0"],  # Binary 0
    ["10", "1"],  # Binary 1
    ["23", ""],  # Footer
]

# Mapping for encoding.
binary2pulses_mapping = {"0": "01", "1": "10"}

name = "rolling1"
type = RFControlProtocolTypes.ROLLING
brands = ["rollingCode"]
pulse_lengths = [500, 1000, 3000, 7250]
pulse_count = 50


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes, for
            example ``"01101010100101011001101010010110100110100101100123"``.

    Returns:
        Dict with the binary ``code``,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None:
        return None

    return {"code": binary}


def encode(code_on: list[str], code_off: list[str], state: bool) -> str:
    """Encode a message into a pulse sequence.

    Args:
        code_on: Recorded binary codes for on; the first one is sent.
        code_off: Recorded binary codes for off; the first one is sent.
        state: True for on, False for off.

    Returns:
        Pulse sequence string.
    """
    code = code_on[0] if state is True else code_off[0]
    return binary2pulses(code, binary2pulses_mapping) + "23"
