"""Stage20 frozen packet-image encoder.

Scientific lock:
    Stage20-1D0
Numeric geometry freeze:
    Stage20-1D3
Verification protocol:
    Stage20-1D4-A

This module contains no label logic and no train/validation/holdout branching.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np


ROWS = 64
COLS = 256
CHANNELS = 1

IPV4_IDENTIFICATION = (4, 6)
IPV4_HEADER_CHECKSUM = (10, 12)
IPV4_SOURCE_ADDRESS = (12, 16)
IPV4_DESTINATION_ADDRESS = (16, 20)

TCP_SEQUENCE_NUMBER = (4, 8)
TCP_ACKNOWLEDGEMENT_NUMBER = (8, 12)
TCP_CHECKSUM = (16, 18)

UDP_CHECKSUM = (6, 8)


def _zero_range(
    buf: bytearray,
    start: int,
    end: int,
    masked_positions: set[int],
) -> None:
    """Zero authentic positions in [start, end), clipped to packet length."""
    start = max(0, int(start))
    end = min(len(buf), int(end))

    if end <= start:
        return

    for pos in range(start, end):
        buf[pos] = 0
        masked_positions.add(pos)


def mask_ipv4_packet(
    packet: bytes | bytearray | memoryview,
) -> tuple[bytes, frozenset[int]]:
    """Apply the frozen Stage20 header masks to one authentic IPv4 packet."""
    source = bytes(packet)

    if len(source) < 20:
        raise ValueError("IPv4 packet shorter than minimum 20-byte header")

    version_ihl = source[0]
    version = version_ihl >> 4
    ihl_words = version_ihl & 0x0F
    ihl_bytes = ihl_words * 4

    if version != 4:
        raise ValueError("packet does not begin with IPv4")

    if ihl_bytes < 20:
        raise ValueError("invalid IPv4 IHL")

    if len(source) < ihl_bytes:
        raise ValueError("captured packet shorter than IPv4 header")

    output = bytearray(source)
    masked_positions: set[int] = set()

    _zero_range(
        output,
        *IPV4_IDENTIFICATION,
        masked_positions,
    )
    _zero_range(
        output,
        *IPV4_HEADER_CHECKSUM,
        masked_positions,
    )
    _zero_range(
        output,
        *IPV4_SOURCE_ADDRESS,
        masked_positions,
    )
    _zero_range(
        output,
        *IPV4_DESTINATION_ADDRESS,
        masked_positions,
    )

    raw_ip_protocol = source[9]

    flags_fragment = int.from_bytes(
        source[6:8],
        "big",
    )

    fragment_offset = (
        flags_fragment
        &
        0x1FFF
    )

    transport_start = ihl_bytes

    if (
        raw_ip_protocol == 6
        and
        fragment_offset == 0
        and
        len(source) >= transport_start + 20
    ):
        _zero_range(
            output,
            transport_start + TCP_SEQUENCE_NUMBER[0],
            transport_start + TCP_SEQUENCE_NUMBER[1],
            masked_positions,
        )
        _zero_range(
            output,
            transport_start + TCP_ACKNOWLEDGEMENT_NUMBER[0],
            transport_start + TCP_ACKNOWLEDGEMENT_NUMBER[1],
            masked_positions,
        )
        _zero_range(
            output,
            transport_start + TCP_CHECKSUM[0],
            transport_start + TCP_CHECKSUM[1],
            masked_positions,
        )

    elif (
        raw_ip_protocol == 17
        and
        fragment_offset == 0
        and
        len(source) >= transport_start + 8
    ):
        _zero_range(
            output,
            transport_start + UDP_CHECKSUM[0],
            transport_start + UDP_CHECKSUM[1],
            masked_positions,
        )

    return (
        bytes(output),
        frozenset(masked_positions),
    )


def encode_flow(
    packets: Sequence[
        bytes | bytearray | memoryview
    ],
) -> tuple[np.ndarray, np.ndarray]:
    """Encode one source-faithful flow with frozen Stage20 semantics."""
    image = np.zeros(
        (ROWS, COLS),
        dtype=np.uint8,
    )

    padding_mask = np.zeros(
        (ROWS, COLS),
        dtype=np.bool_,
    )

    for row_index, packet in enumerate(
        packets[:ROWS]
    ):
        source = bytes(packet)

        masked_packet, _ = mask_ipv4_packet(
            source
        )

        retained_length = min(
            len(masked_packet),
            COLS,
        )

        if retained_length > 0:
            image[
                row_index,
                :retained_length,
            ] = np.frombuffer(
                masked_packet[
                    :retained_length
                ],
                dtype=np.uint8,
            )

            padding_mask[
                row_index,
                :retained_length,
            ] = True

    return image, padding_mask


def scale_for_model(
    image: np.ndarray,
) -> np.ndarray:
    """Frozen model-boundary scaling: float(image) / 255.0."""
    array = np.asarray(image)

    if array.shape != (ROWS, COLS):
        raise ValueError(
            f"expected {(ROWS, COLS)}, got {array.shape}"
        )

    return (
        array.astype(np.float32)
        /
        np.float32(255.0)
    )
