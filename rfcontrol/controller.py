"""
Python port of the original CoffeeScript/nodejs code
"""

# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import

import glob
import logging
from os.path import basename, dirname, isfile, join

import rfcontrol.protocols
from rfcontrol.protocols import *

logger = logging.getLogger(__name__)

protocols = [
    getattr(rfcontrol.protocols, basename(f)[:-3])
    for f in glob.glob(join(dirname(__file__), "protocols/*.py"))
    if isfile(f) and not basename(f).startswith("_")
]


class RFControlError(Exception):
    """
    Generic RF Control error.
    """


class RFControlProtocolNotFoundError(RFControlError):
    """
    This error is raised when a protocol can not be found.
    """


class RFControlSendNotSupportedError(RFControlError):
    """
    This error is raised when a protocol only supports receiving and not sending.
    """


def does_protocol_match(pulse_lengths, pulse_sequence, protocol) -> bool:
    """
    Test if a protocol matches the pulse lengths and pulse sequence
    """
    if protocol.pulse_count != len(pulse_sequence):
        return False

    if len(protocol.pulse_lengths) != len(pulse_lengths):
        return False

    for i, pulse_length in enumerate(pulse_lengths):
        max_delta = pulse_length * 0.4
        if abs(protocol.pulse_lengths[i] - pulse_length) > max_delta:
            return False

    return True


def sort_indices(array: []):
    """
    Sort the indexes of an array by order of element value.
    """
    sorted_indices = [i for i, _ in sorted(enumerate(array), key=lambda x: x[1])]
    # logger.debug("sorted indices: %s", sorted_indices)

    return sorted_indices


def compress_timings(timings: []):
    """
    Compress timings.
    """
    pulses = ""
    buckets = []
    sums = []
    counts = []

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


def prepare_compressed_pulses(input: str):
    """
    Prepares compressed pulses.
    """
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


def sort_compressed_pulses(pulse_lengths: [], pulse_sequence: str):
    """
    Sort the pulse lengths from short to long and updates indices in pulse sequence accordingly.
    """
    # Sort the pulse lengths from short to long.
    sorted_indices = sort_indices(pulse_lengths)
    pulse_lengths.sort()

    # Updates indices in pulse sequence accordingly.
    reindexed_pulse_sequence = ""
    for c in pulse_sequence:
        reindexed_pulse_sequence += str(sorted_indices.index(int(c)))
    # logger.debug("reindexed pulse sequence: %s", reindexed_pulse_sequence)

    return (pulse_lengths, reindexed_pulse_sequence)


def fix_pulses(pulse_lengths: [], pulse_sequence: str):
    """
    Merge pulse timings with similar length.

    Timings are considered the same if they differ less then a factor of 2.
    """
    # If we have less then 3 different pulseLenght there is nothing to fix.
    if len(pulse_lengths) <= 3:
        return None

    # Consider timing as the same if they differ less then a factor of 2.
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
    if i is len(pulse_lengths):
        return None

    # Adapt pulses
    new_pulse_sequence = pulse_sequence
    while i < len(pulse_lengths):
        new_pulse_sequence = new_pulse_sequence.replace(f"{i}", f"{i-1}")
        i += 1
    return (new_pulse_lengths, new_pulse_sequence)


def decode_pulses(pulse_lengths: [], pulse_sequence: str):
    """
    Decode pulse sequence to protocol
    """
    # Filter out 0 length pulses
    pulse_lengths = [i for i in pulse_lengths if i > 0]
    # logger.debug("Non 0 pulse lengths: %s", pulse_lengths)

    pulse_lengths, pulse_sequence = sort_compressed_pulses(
        pulse_lengths, pulse_sequence
    )

    return _decode_pulses(pulse_lengths, pulse_sequence)


def _decode_pulses(pulse_lengths: [], pulse_sequence: str):
    results = []
    for protocol in protocols:
        if does_protocol_match(pulse_lengths, pulse_sequence, protocol):
            decoded = protocol.decode(pulse_sequence)
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


def encode_pulses(protocol_name: str, message: str):
    """
    Encode protocol to pulse sequence
    """
    protocol = get_protocol(protocol_name)

    if protocol is None:
        raise RFControlProtocolNotFoundError(
            f"Could not find a protocol named {protocol_name}"
        )

    if protocol.encode is None:
        raise RFControlSendNotSupportedError("The protocol has no send support")

    return {
        "pulses": protocol.encode(**message),
        "pulse_lengths": protocol.pulse_lengths,
    }


def get_all_protocols() -> []:
    """
    Get all implemented protocols.
    """
    return protocols


def get_protocol(protocol_name: str) -> str | None:
    """
    Get protocol with given name.
    """
    return getattr(rfcontrol.protocols, protocol_name, None)
