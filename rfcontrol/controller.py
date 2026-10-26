"""Decode and encode RF pulse sequences.

Python port of the original CoffeeScript/Node.js rfcontroljs controller.
"""

from collections.abc import Sequence
import importlib
import logging
from pathlib import Path
from types import ModuleType
from typing import Any

logger = logging.getLogger(__name__)

protocols: list[ModuleType] = [
    importlib.import_module(f"rfcontrol.protocols.{f.stem}")
    for f in (Path(__file__).parent / "protocols").glob("*.py")
    if f.is_file() and not f.name.startswith("_")
]


def __getattr__(name: str) -> ModuleType:
    """Give access to the protocol modules as attributes of this module.

    Kept for backward compatibility with code that looks protocols up as
    ``controller.<protocol>`` or ``getattr(controller, "<protocol>")``, like
    homeduino does.
    """
    protocol = get_protocol(name)
    if protocol is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    return protocol


class RFControlError(Exception):
    """Generic RF Control error."""


class RFControlProtocolNotFoundError(RFControlError):
    """This error is raised when a protocol can not be found."""


class RFControlSendNotSupportedError(RFControlError):
    """This error is raised when a protocol only supports receiving and not sending."""


def does_protocol_match(
    pulse_lengths: list[int], pulse_sequence: str, protocol: ModuleType
) -> bool:
    """Test if a protocol matches the pulse lengths and pulse sequence."""
    pulse_counts = getattr(protocol, "pulse_counts", None)
    if pulse_counts is not None:
        if len(pulse_sequence) not in pulse_counts:
            return False
    elif protocol.pulse_count != len(pulse_sequence):
        return False

    if len(protocol.pulse_lengths) != len(pulse_lengths):
        return False

    for i, pulse_length in enumerate(pulse_lengths):
        max_delta = pulse_length * 0.4
        if abs(protocol.pulse_lengths[i] - pulse_length) > max_delta:
            return False

    return True


def sort_indices(array: Sequence[int]) -> list[int]:
    """Sort the indexes of an array by order of element value."""
    return [i for i, _ in sorted(enumerate(array), key=lambda x: x[1])]


def compress_timings(timings: list[int]) -> tuple[list[int], str]:
    """Compress timings."""
    pulses = ""
    buckets: list[int] = []
    sums: list[int] = []
    counts: list[int] = []

    for timing in timings:
        # Search for a bucket.
        has_match = False
        for j, bucket in enumerate(buckets):
            if abs(bucket - timing) < bucket * 0.5:
                pulses += str(j)
                sums[j] += timing
                counts[j] += 1
                has_match = True
        if not has_match:
            # Create new bucket.
            pulses += str(len(buckets))
            buckets.append(timing)
            sums.append(timing)
            counts.append(1)

    for j, _bucket in enumerate(buckets):
        buckets[j] = round(sums[j] / counts[j])

    return (buckets, pulses)


def prepare_compressed_pulses(input: str) -> tuple[list[int], str]:
    """Prepares compressed pulses."""
    # Input is something like:
    # 268 2632 1282 10168 0 0 0 0 010002000202000002000200020200020002...
    # The first 8 numbers are the pulse length and the last string is the pulse sequence
    parts = input.split(" ")
    pulse_lengths = [int(i) for i in parts[0:8]]
    pulse_sequence = parts[8]

    # Now lets filter out 0 pulses
    pulse_lengths = list(filter(lambda pulse_length: pulse_length > 0, pulse_lengths))

    # Next sort the pulses from short to long and update indices in pulses.
    return sort_compressed_pulses(pulse_lengths, pulse_sequence)


def sort_compressed_pulses(
    pulse_lengths: list[int], pulse_sequence: str
) -> tuple[list[int], str]:
    """Sort the pulse lengths from short to long and updates indices in pulse sequence accordingly."""
    # Sort the pulse lengths from short to long.
    sorted_indices = sort_indices(pulse_lengths)
    pulse_lengths.sort()

    # Updates indices in pulse sequence accordingly.
    reindexed_pulse_sequence = ""
    for c in pulse_sequence:
        reindexed_pulse_sequence += str(sorted_indices.index(int(c)))

    return (pulse_lengths, reindexed_pulse_sequence)


def fix_pulses(
    pulse_lengths: list[int], pulse_sequence: str
) -> tuple[list[int], str] | None:
    """Merge pulse timings with similar length.

    Timings are considered the same if they differ less than a factor of 2.
    """
    # If we have less than 3 different pulse lengths there is nothing to fix.
    if len(pulse_lengths) <= 3:
        return None

    # Consider timing as the same if they differ less than a factor of 2.
    i = 1
    while i < len(pulse_lengths):
        if pulse_lengths[i - 1] * 2 < pulse_lengths[i]:
            i += 1
            continue
        # Merge pulseLengths[i-1] and pulseLengths[i]
        new_pulse_length = int((pulse_lengths[i - 1] + pulse_lengths[i]) / 2)
        # Replace the old two pulse length with the new one
        new_pulse_lengths = pulse_lengths[: i - 1]
        new_pulse_lengths.append(new_pulse_length)
        new_pulse_lengths.extend(pulse_lengths[i + 1 :])
        break

    # Nothing to do...
    if i == len(pulse_lengths):
        return None

    # Adapt pulses
    new_pulse_sequence = pulse_sequence
    while i < len(pulse_lengths):
        new_pulse_sequence = new_pulse_sequence.replace(f"{i}", f"{i - 1}")
        i += 1
    return (new_pulse_lengths, new_pulse_sequence)


def decode_pulses(
    pulse_lengths: list[int], pulse_sequence: str
) -> list[dict[str, Any]]:
    """Decode a pulse sequence to protocol messages."""
    # Filter out 0 length pulses
    pulse_lengths = [i for i in pulse_lengths if i > 0]

    if not set(pulse_sequence) <= {str(i) for i in range(len(pulse_lengths))}:
        logger.debug("Pulse sequence refers to unknown pulse lengths")
        return []

    pulse_lengths, pulse_sequence = sort_compressed_pulses(
        pulse_lengths, pulse_sequence
    )

    return _decode_pulses(pulse_lengths, pulse_sequence)


def _decode_pulses(
    pulse_lengths: list[int], pulse_sequence: str
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for protocol in protocols:
        if does_protocol_match(pulse_lengths, pulse_sequence, protocol):
            try:
                decoded = protocol.decode(pulse_sequence)
            except IndexError, KeyError, ValueError:
                logger.debug("Protocol %s failed to decode the pulses", protocol.name)
                continue
            if decoded is not None:
                logger.debug("Protocol %s matches", protocol.name)
                logger.debug("Decoded reception: %s", decoded)
                results.append({"protocol": protocol.name, "values": decoded})

    # Try to fix pulses.
    fixed_pulses = fix_pulses(pulse_lengths, pulse_sequence)
    if fixed_pulses is not None:
        # We have fixes so try again with the fixed pulse lengths...
        results.extend(_decode_pulses(fixed_pulses[0], fixed_pulses[1]))

    return results


def encode_pulses(protocol_name: str, message: dict[str, Any]) -> dict[str, Any]:
    """Encode a protocol message to a pulse sequence."""
    protocol = get_protocol(protocol_name)

    if protocol is None:
        raise RFControlProtocolNotFoundError(
            f"Could not find a protocol named {protocol_name}"
        )

    if getattr(protocol, "encode", None) is None:
        raise RFControlSendNotSupportedError("The protocol has no send support")

    return {
        "pulses": protocol.encode(**message),
        "pulse_lengths": protocol.pulse_lengths,
    }


def get_all_protocols() -> list[ModuleType]:
    """Get all implemented protocols."""
    return protocols


def get_protocol(protocol_name: str) -> ModuleType | None:
    """Get protocol with given name, or None if there is no such protocol."""
    for protocol in protocols:
        if protocol.name == protocol_name:
            return protocol
    return None
