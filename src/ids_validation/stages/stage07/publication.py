"""Read-only Stage 7 publication inventory and historical packaging declarations."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ids_validation.common.hashing import sha256_file


GENERATED_FIGURES = (
    "figures/figure01_baseline16_f1_comparison.png",
    "figures/figure02_tuned_top5_f1_comparison.png",
    "figures/figure03_constrained_security_f2_comparison.png",
    "figures/figure04_xgboost_threshold_tradeoff.png",
    "figures/figure05_lightgbm_threshold_tradeoff.png",
    "figures/figure06_final_holdout_objective_comparison.png",
    "figures/figure07_xgboost_holdout_confusion_matrix.png",
    "figures/figure08_lightgbm_security_confusion_matrix.png",
    "figures/figure09_shap_rank_agreement.png",
)

COPIED_SHAP_FIGURES = (
    "figures/xgboost_shap_summary_plot.png",
    "figures/xgboost_shap_top20_bar_plot.png",
    "figures/xgboost_shap_attack_waterfall.png",
    "figures/lightgbm_shap_summary_plot.png",
    "figures/lightgbm_shap_top20_bar_plot.png",
    "figures/lightgbm_shap_attack_waterfall.png",
)

PUBLICATION_TABLE_BASENAMES = (
    "table01_baseline16_validation_results",
    "table02_tuned_top5_validation_results",
    "table03_constrained_security_validation_results",
    "table04_objective_specific_holdout_results",
)

CSV_TABLES = tuple(f"tables/{name}.csv" for name in PUBLICATION_TABLE_BASENAMES)
LATEX_TABLES = tuple(f"tables/{name}.tex" for name in PUBLICATION_TABLE_BASENAMES)


def expected_publication_artifacts() -> tuple[str, ...]:
    """Return the exact Stage 7 inventory of 15 figures and eight tables.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 109
    Original stage: Stage 7
    Frozen artifacts generated: figures/figure01_baseline16_f1_comparison.png through figures/figure09_shap_rank_agreement.png, tables/table01_baseline16_validation_results.* through tables/table04_objective_specific_holdout_results.*
    Notes: Six SHAP figures were copied from Stage 6, while nine figures and eight tables were generated in Stage 7.
    """

    return GENERATED_FIGURES + COPIED_SHAP_FIGURES + CSV_TABLES + LATEX_TABLES


def verify_expected_publication_artifacts(repository_root: Path | str) -> list[dict[str, Any]]:
    """Check Stage 7 publication artifact presence without reading payloads.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 109, 115
    Original stage: Stage 7
    Frozen artifacts generated: metadata/publication_assets_metadata.json
    Notes: This verify-only adaptation performs no figure/table regeneration and opens no scientific input.
    """

    root = Path(repository_root).resolve()
    return [{"path": relative, "exists": (root / relative).exists()} for relative in expected_publication_artifacts()]


def inventory_files(root: Path | str) -> list[dict[str, Any]]:
    """Build the Stage 7 sorted size/SHA-256 file inventory.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 112
    Original stage: Stage 7
    Frozen artifacts generated: complete_working_manifest.json
    Notes: Safe for temporary/toy directories; canonical entry points do not run full-repository hashing.
    """

    base = Path(root).resolve()
    inventory = []
    for path in sorted(base.rglob("*")):
        if not path.is_file():
            continue
        inventory.append(
            {
                "path": path.relative_to(base).as_posix(),
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return inventory


def zip_cleanup_candidates(root: Path | str) -> tuple[Path, ...]:
    """List historical Stage 7 ZIP cleanup targets without deleting them.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 110
    Original stage: Stage 7
    Frozen artifacts generated: None recorded
    Notes: Cell 110 called unlink on every ZIP under /kaggle/working; extraction intentionally exposes discovery only.
    """

    return tuple(sorted(path for path in Path(root).rglob("*.zip") if path.is_file()))


def complete_archive_command(working_directory: Path | str, temporary_archive: Path | str) -> tuple[str, ...]:
    """Return, but never execute, the exact historical tar command.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 113
    Original stage: Stage 7
    Frozen artifacts generated: ids2018_validation_safe_complete_working.tar.gz
    Notes: Archive creation and overwrite/removal behavior remain disabled in this phase.
    """

    return ("tar", "-czf", str(temporary_archive), "-C", str(working_directory), ".")


def archive_checksum_line(archive_name: str, digest: str) -> str:
    """Render the Stage 7 SHA-256 checksum-file line.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 113
    Original stage: Stage 7
    Frozen artifacts generated: ids2018_validation_safe_complete_working.tar.gz.sha256
    Notes: Pure formatting helper; it does not create or open an archive.
    """

    return f"{digest}  {archive_name}\n"
