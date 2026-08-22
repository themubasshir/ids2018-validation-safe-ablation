"""Deterministic Stage20-1D toy packet-row encoder.

The helper accepts caller-supplied byte strings beginning at IPv4 byte zero. It
does not parse PCAP files, reconstruct flows, join labels, or open artifacts.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np


PACKET_ROWS = 64
BYTE_COLUMNS = 256
CHANNELS = 1


def _zero_interval(row: np.ndarray, authentic_length: int, start: int, stop: int) -> None:
    row[start : min(stop, authentic_length)] = 0


def _mask_authentic_headers(row: np.ndarray, packet: bytes, authentic_length: int) -> None:
    for start, stop in ((4, 6), (10, 12), (12, 16), (16, 20)):
        _zero_interval(row, authentic_length, start, stop)
    if len(packet) < 20 or packet[0] >> 4 != 4:
        return
    transport_start = (packet[0] & 0x0F) * 4
    fragment_offset = int.from_bytes(packet[6:8], "big") & 0x1FFF
    protocol = packet[9]
    if transport_start < 20 or fragment_offset != 0:
        return
    if protocol == 6 and len(packet) >= transport_start + 20:
        for start, stop in ((4, 8), (8, 12), (16, 18)):
            _zero_interval(row, authentic_length, transport_start + start, transport_start + stop)
    elif protocol == 17 and len(packet) >= transport_start + 8:
        _zero_interval(row, authentic_length, transport_start + 6, transport_start + 8)


def encode_packet_rows(packets: Sequence[bytes]) -> tuple[np.ndarray, np.ndarray]:
    """Encode toy captured-IPv4 packet bytes as one 64x256 uint8 image.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 412, 420, 421, 422
    Original stage: Stage20-1D0/1D3/1D4
    Frozen artifacts generated: stage20_1d0_packet_image_representation_selection_lock.json, stage20_1d4a_fixed_encoder_verification_protocol_lock.json
    Notes: Earliest packets/bytes are retained. The mask remains true at
    authentic zero or masked positions and false only for right/bottom padding.
    """

    image = np.zeros((PACKET_ROWS, BYTE_COLUMNS), dtype=np.uint8)
    padding_mask = np.zeros((PACKET_ROWS, BYTE_COLUMNS), dtype=np.bool_)
    for row_index, packet in enumerate(packets[:PACKET_ROWS]):
        if not isinstance(packet, bytes):
            raise TypeError("each packet must be a bytes object beginning at IPv4 byte zero")
        authentic_length = min(len(packet), BYTE_COLUMNS)
        image[row_index, :authentic_length] = np.frombuffer(packet[:authentic_length], dtype=np.uint8)
        padding_mask[row_index, :authentic_length] = True
        _mask_authentic_headers(image[row_index], packet, authentic_length)
    return image, padding_mask


def scale_for_model(image: np.ndarray) -> np.ndarray:
    """Apply only the frozen model-boundary byte/255 scaling to a toy image.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 412, 421, 422, 423
    Original stage: Stage20-1D0/1D4 and Stage20-1E0
    Frozen artifacts generated: stage20_1d4a_fixed_encoder_verification_protocol_lock.json, stage20_1e0_architecture_training_protocol_lock.json
    Notes: This accepts only an already-encoded toy uint8 image; it performs no
    packet parsing, corpus loading, model forward pass, or inference.
    """

    array = np.asarray(image)
    if array.shape != (PACKET_ROWS, BYTE_COLUMNS) or array.dtype != np.uint8:
        raise ValueError("image must be a uint8 array with shape (64, 256)")
    return array.astype(np.float32) / 255.0
