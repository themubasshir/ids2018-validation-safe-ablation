"""Static CICIDS2017 provenance recorded by Stage 20.

Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
Original physical cells: 313–326, 331–335, 414, 417–418, 424–434, 455
Frozen artifacts: Stage20 1B3 label hygiene, 1D daily geometry profiles, and
1E compact-corpus manifests.  This module opens none of those scientific files.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceArtifact:
    """Byte identity and historical role of one remote source artifact."""

    split: str
    day: str
    path: str
    revision: str
    size_bytes: int | None
    sha256: str
    status: str = "FROZEN_REPOSITORY_EVIDENCE"


PCAP_REVISION = "e810c1cc98270ec271a1df917b9de0786c33f343"
LABEL_REVISION = "b7e532345512edcd530cb1770dc76636aeb52802"

DEVELOPMENT_PCAPS = (
    SourceArtifact("TRAIN", "Monday", "pcap/Monday-WorkingHours.pcap", PCAP_REVISION, None, "f6eac599358f216b074338813a1cf7be3cc4e91d116e13efc0dc71f2cca11972"),
    SourceArtifact("TRAIN", "Tuesday", "pcap/Tuesday-WorkingHours.pcap", PCAP_REVISION, None, "080c2250154c5a174c03660ed0f75a3858d41a27511ba716e780d7bcb1ec4c57"),
    SourceArtifact("TRAIN", "Wednesday", "pcap/Wednesday-workingHours.pcap", PCAP_REVISION, None, "cd2674db7559a53f24bc03be3239b315700174ccaef72d10f5edc4c1a08f6186"),
    SourceArtifact("VALIDATION", "Thursday", "pcap/Thursday-WorkingHours.pcap", PCAP_REVISION, 8_302_500_180, "38f8b1bb276849bf1721f7c4de22bebfa7f59a74e52286d4c0a37edbb118fe01"),
)

HOLDOUT_PCAP = SourceArtifact(
    "HOLDOUT",
    "Friday",
    "pcap/Friday-WorkingHours.pcap",
    PCAP_REVISION,
    None,
    "beff0dcce1eebc9b2454582f4dc8ed0ba0112b2c619a710bf03af93147254cd0",
    status="LATER_FROZEN_EVIDENCE_NOTEBOOK_CELL_NOT_MAPPED",
)

CANONICAL_LABEL_TABLES = (
    SourceArtifact("TRAIN", "Monday", "traffic_labels/Monday-WorkingHours.pcap_ISCX.csv.parquet", LABEL_REVISION, 65_465_382, "dfdcef4b8670e52af54dc4f82174834365a393473e877174cca46d17b12dfd02"),
    SourceArtifact("TRAIN", "Tuesday", "traffic_labels/Tuesday-WorkingHours.pcap_ISCX.csv.parquet", LABEL_REVISION, 52_701_751, "27e83d518cb093faefd0f883cb4df3ad8b353f150934004f28d0e7962f9f31c4"),
    SourceArtifact("TRAIN", "Wednesday", "traffic_labels/Wednesday-workingHours.pcap_ISCX.csv.parquet", LABEL_REVISION, 76_512_727, "d23a259820b16e1ad54f9f3b58d5727c5032d383015f90bc7c07cebbdf8a7140"),
    SourceArtifact("VALIDATION", "Thursday morning", "traffic_labels/Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv.parquet", LABEL_REVISION, 19_674_280, "d8110c04a7af91124ada1c5ad901c4210879df1af8882dc637767532e7165350"),
    SourceArtifact("VALIDATION", "Thursday afternoon", "traffic_labels/Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv.parquet", LABEL_REVISION, 27_901_448, "5da010354f0fc1040fd1fe65967096e1063475de8dd30ae4f657c07201d728a7"),
)

CANONICAL_LABEL_CONTENT_HASHES = {
    "Monday": "2ab16b8d851e002c1b149ede2b952777cedae6e57f815441ad4c6090ea96ac70",
    "Tuesday": "28ca517d154a672dd9dd5a61e34e663e968b15f9d28b43a79076cf67854366c6",
    "Wednesday": "898c16c2bf6eef3e757a25bad7e56c531cc1de1ecb65e538679ef34d9a400b22",
    "Thursday morning": "a183fb9a4f569e694ec6f296d2c396db436999bd55813fc2443597b3462e2b4f",
    "Thursday afternoon": "1dd0b69281b8ddb6cf53c00a0391c81424b513b1f69709e7c89d6b540c3c3c56",
}
