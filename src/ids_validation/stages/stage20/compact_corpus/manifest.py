"""Static Stage20-1E1 compact-corpus identities."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CorpusFile:
    """Frozen byte count and digest for one compact-corpus component."""

    name: str
    size_bytes: int
    sha256: str


@dataclass(frozen=True)
class CompactCorpusReceipt:
    """Frozen metadata for one historically materialized day corpus."""

    day: str
    split: str
    flow_count: int
    encoded_authentic_bytes: int
    files: tuple[CorpusFile, ...]
    provenance: str = "DIRECT_NOTEBOOK_AND_ARTIFACT"


CORPUS_RECEIPTS = (
    CompactCorpusReceipt(
        "Monday", "TRAIN", 528_509, 522_845_159,
        (
            CorpusFile("encoded_bytes.bin", 522_845_159, "27e6f730c9951075f500bedc96b91d215b74a995ee23e1f09e269eaa7a2bd82c"),
            CorpusFile("flow_offsets.npy", 4_228_208, "3744c55767896e98f5691210d6820224d9ae8315130ce74bb5d4264c25e4326e"),
            CorpusFile("labels.npy", 528_637, "48792b8d6a127b35342cb0789baa6c54396f1100a60ce7225daf08d1c3530424"),
            CorpusFile("packet_lengths.npy", 67_649_280, "16547aedafc3aaffcf9dca5ef50c7456cd823ed1ab59965a4c10520f11fb68f8"),
        ),
    ),
    CompactCorpusReceipt(
        "Tuesday", "TRAIN", 4_170, 4_078_271,
        (
            CorpusFile("encoded_bytes.bin", 4_078_271, "cbfe435fe612e1a5e6f8dc44e5a6694cf1ce6efbe0dc6e89c5c62e4dc5da4f48"),
            CorpusFile("flow_offsets.npy", 33_496, "4b9334dc876362b8937d21de276a03654e275b94a2c6fc4b23e0881d4d518be9"),
            CorpusFile("labels.npy", 4_298, "e8891a80aea004b84cffb3fa4c53a71d32ae96796ac052e7073530a1b0cc9fff"),
            CorpusFile("packet_lengths.npy", 533_888, "058641aa2e24aa9a308fd553ecae571867c478063dfe1261551285d81965808c"),
        ),
    ),
    CompactCorpusReceipt(
        "Wednesday", "TRAIN", 12_951, 13_824_937,
        (
            CorpusFile("encoded_bytes.bin", 13_824_937, "b4ba9a059a2df6a1b85546b4d92c1fdf5b80feb61de6c3e56eae458c628f8889"),
            CorpusFile("flow_offsets.npy", 103_744, "9ef83af5b03f9284beed50cbe2587bbbb8cac1ac524aa5505e44d262a8d8cf0a"),
            CorpusFile("labels.npy", 13_079, "9d10b0264487ab4689a77f0101f22496786a7eb453236c2fb8bfe53d33f9ca7c"),
            CorpusFile("packet_lengths.npy", 1_657_856, "9bba88e143d4c5c5388c450b1f7d7c9aa1cd83592c4c6e1a153651e70131d2ab"),
        ),
    ),
    CompactCorpusReceipt(
        "Thursday", "VALIDATION", 8_197, 7_586_531,
        (
            CorpusFile("encoded_bytes.bin", 7_586_531, "2593b328839ecf28d901242b6850474fa028484656c7235ff78ef2b437c01ca0"),
            CorpusFile("flow_offsets.npy", 65_712, "137d38b8bfdcd22986e954f7b39ae4383da33b6194998ebb8fc8b63b3259e522"),
            CorpusFile("labels.npy", 8_325, "cb1c6b3bf716ed9244029b5866ac3d0ca8da8b9bc152f8e89d5b1d6c78e5ec6e"),
            CorpusFile("packet_lengths.npy", 1_049_344, "db195558d0a12f74e8d4ba8c1ccd7ee4b322993b42575793761c6991fdb1f21c"),
        ),
    ),
)

FORMAT = "STAGE20_1E0_COMPACT_VARIABLE_AUTHENTIC_BYTES"
ENCODER_SHA256 = "9883fe2b27020aaff707a753123b35eb3223d21abf295d056ec233e532f94222"
LOADER_SHA256 = "a1ba15881afeb1cf4de9225a06df9ae676b95f596c8ddced7734a445ba7624d0"
DENSE_PADDING_PERSISTED = False
PADDING_MASK_RECONSTRUCTED_FROM_LENGTHS = True
