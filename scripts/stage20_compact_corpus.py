"""Stage20 compact packet-image corpus loader.

Format frozen by Stage20-1E0.

The corpus does not persist dense zero padding.  It stores only the authentic,
already-masked retained byte prefixes plus a [N,64] uint16 length matrix.
This loader reconstructs exactly the 64x256 uint8 image and Boolean padding
mask expected by the frozen Stage20 encoder/model.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np


ROWS = 64
COLS = 256


class Stage20CompactCorpus:
    """Memory-mapped reader for one materialized Stage20 source-day corpus."""

    def __init__(self, directory: str | Path) -> None:
        self.directory = Path(directory)

        self.encoded_path = (
            self.directory
            / "encoded_bytes.bin"
        )

        self.lengths_path = (
            self.directory
            / "packet_lengths.npy"
        )

        self.offsets_path = (
            self.directory
            / "flow_offsets.npy"
        )

        self.labels_path = (
            self.directory
            / "labels.npy"
        )

        for path in (
            self.encoded_path,
            self.lengths_path,
            self.offsets_path,
            self.labels_path,
        ):
            if not path.is_file():
                raise FileNotFoundError(path)

        self.packet_lengths = np.load(
            self.lengths_path,
            mmap_mode="r",
            allow_pickle=False,
        )

        self.flow_offsets = np.load(
            self.offsets_path,
            mmap_mode="r",
            allow_pickle=False,
        )

        self.labels = np.load(
            self.labels_path,
            mmap_mode="r",
            allow_pickle=False,
        )

        if (
            self.packet_lengths.ndim != 2
            or
            self.packet_lengths.shape[1] != ROWS
        ):
            raise ValueError(
                "packet_lengths.npy must have shape [N,64]"
            )

        self._n = int(
            self.packet_lengths.shape[0]
        )

        if self.labels.shape != (
            self._n,
        ):
            raise ValueError(
                "labels.npy length does not match packet_lengths.npy"
            )

        if self.flow_offsets.shape != (
            self._n + 1,
        ):
            raise ValueError(
                "flow_offsets.npy must have shape [N+1]"
            )

        if self.packet_lengths.dtype != np.uint16:
            raise ValueError(
                "packet_lengths.npy must be uint16"
            )

        if self.flow_offsets.dtype != np.uint64:
            raise ValueError(
                "flow_offsets.npy must be uint64"
            )

        if self.labels.dtype != np.uint8:
            raise ValueError(
                "labels.npy must be uint8"
            )

        encoded_size = int(
            self.encoded_path.stat().st_size
        )

        if int(
            self.flow_offsets[0]
        ) != 0:
            raise ValueError(
                "first flow offset must be zero"
            )

        if int(
            self.flow_offsets[-1]
        ) != encoded_size:
            raise ValueError(
                "final flow offset does not equal encoded_bytes.bin size"
            )

        self.encoded_bytes = np.memmap(
            self.encoded_path,
            dtype=np.uint8,
            mode="r",
            shape=(encoded_size,),
        )

    def __len__(self) -> int:
        return self._n

    def reconstruct(
        self,
        index: int,
    ) -> tuple[np.ndarray, np.ndarray, int]:
        """Return dense uint8 image, bool padding mask, and uint8 label."""

        index = int(index)

        if index < 0:
            index += self._n

        if (
            index < 0
            or
            index >= self._n
        ):
            raise IndexError(index)

        lengths = np.asarray(
            self.packet_lengths[
                index
            ],
            dtype=np.uint16,
        )

        if np.any(
            lengths > COLS
        ):
            raise ValueError(
                "packet length exceeds frozen 256-byte width"
            )

        start = int(
            self.flow_offsets[
                index
            ]
        )

        end = int(
            self.flow_offsets[
                index + 1
            ]
        )

        expected = int(
            lengths.astype(
                np.uint64
            ).sum()
        )

        if end - start != expected:
            raise ValueError(
                "flow offset delta does not equal sum(packet_lengths)"
            )

        image = np.zeros(
            (
                ROWS,
                COLS,
            ),
            dtype=np.uint8,
        )

        padding_mask = np.zeros(
            (
                ROWS,
                COLS,
            ),
            dtype=np.bool_,
        )

        cursor = start

        for row_index, length in enumerate(
            lengths.tolist()
        ):
            length = int(
                length
            )

            if length == 0:
                continue

            next_cursor = (
                cursor
                +
                length
            )

            image[
                row_index,
                :length,
            ] = self.encoded_bytes[
                cursor:
                next_cursor
            ]

            padding_mask[
                row_index,
                :length,
            ] = True

            cursor = next_cursor

        if cursor != end:
            raise ValueError(
                "flow byte traversal did not terminate at expected offset"
            )

        label = int(
            self.labels[
                index
            ]
        )

        if label not in (
            0,
            1,
        ):
            raise ValueError(
                f"invalid binary label {label}"
            )

        return (
            image,
            padding_mask,
            label,
        )
