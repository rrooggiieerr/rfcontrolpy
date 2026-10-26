"""Skeleton protocol to copy when implementing a new protocol."""

from typing import Any

from rfcontrol.helpers import pulses2binary
from rfcontrol.protocols import RFControlProtocolTypes

# Mapping for decoding.
pulses2binary_mapping: list[list[str]] = []

# Mapping for encoding.
binary2pulses_mapping: dict[str, str] = {}

name = "skeleton"
type = RFControlProtocolTypes.DIMMER
brands: list[str] = []
pulse_lengths: list[int] = []
pulse_count = 0


def decode(pulses: str) -> dict[str, Any] | None:
    """Decode a pulse sequence.

    Args:
        pulses: Pulse sequence as a string of pulse-length indexes.

    Returns:
        Dict with the decoded values,
        or None if the pulses don't match the protocol.
    """
    # We first map the sequences to binary.
    binary = pulses2binary(pulses, pulses2binary_mapping)

    if binary is None:
        return None

    # Binary is now something like:
    #

    # Now we extract the data from that string.
    return {}


def encode(id: int, unit: int) -> str:
    """Encode a message into a pulse sequence.

    Args:
        id: Device ID.
        unit: Unit code.

    Returns:
        Pulse sequence string.
    """
    return ""
