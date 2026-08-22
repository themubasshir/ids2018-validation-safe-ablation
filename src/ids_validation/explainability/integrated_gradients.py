"""Stage 14 neural compatibility and Integrated Gradients mathematical helpers."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

import numpy as np


RANDOM_STATE = 42
FEATURE_COUNT = 78
AUDITED_STEP_COUNTS = (16, 32, 64, 128)
MAX_STEPS = 128
SELECTED_INTEGRATION_STEPS = 128
GRADIENT_BATCH_SIZE = 512
REFERENCE_COUNT = 32
TOP_K = 10
ABSOLUTE_COMPLETENESS_TOLERANCE = 0.05
NORMALIZED_COMPLETENESS_TOLERANCE = 0.01


def determine_input_mode(input_shape: Sequence[int | None], feature_count: int = FEATURE_COUNT) -> str:
    """Classify the exact Stage 14 supported MLP/CNN input shapes.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 148
    Original stage: Stage 14
    Frozen artifacts generated: results/stage14_integrated_gradients/stage14_1_neural_model_compatibility.csv
    Notes: Supports flat (None,78), last-channel (None,78,1), and first-channel (None,1,78) single-input models only.
    """

    normalized = tuple(None if value is None else int(value) for value in input_shape)
    if len(normalized) == 2 and normalized[-1] == feature_count:
        return "flat_2d"
    if len(normalized) == 3 and normalized[-2:] == (feature_count, 1):
        return "sequence_3d_last_channel"
    if len(normalized) == 3 and normalized[-2:] == (1, feature_count):
        return "sequence_3d_first_channel"
    raise ValueError(f"Unsupported model input shape: {normalized}")


def prepare_input_for_model(scaled_matrix: np.ndarray, input_mode: str) -> np.ndarray:
    """Reshape scaled features according to the Stage 14 compatibility audit.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 148
    Original stage: Stage 14
    Frozen artifacts generated: results/stage14_integrated_gradients/stage14_1_neural_model_compatibility.csv
    Notes: Pure toy/static shape helper; it never loads or calls a neural model.
    """

    matrix = np.asarray(scaled_matrix, dtype=np.float32)
    if input_mode == "flat_2d":
        return matrix
    if input_mode == "sequence_3d_last_channel":
        return matrix[..., np.newaxis]
    if input_mode == "sequence_3d_first_channel":
        return matrix[:, np.newaxis, :]
    raise ValueError(f"Unknown input mode: {input_mode}")


def normalize_binary_attack_probability(prediction_output: np.ndarray) -> np.ndarray:
    """Normalize Stage 14 neural outputs to the attack-probability vector.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 148
    Original stage: Stage 14
    Frozen artifacts generated: results/stage14_integrated_gradients/stage14_1_archived_neural_file_audit.csv
    Notes: Accepts one-dimensional, Nx1, or Nx2 outputs; Nx2 selects column 1.
    """

    output = np.asarray(prediction_output, dtype=np.float64)
    if output.ndim == 1:
        probability = output
    elif output.ndim == 2 and output.shape[1] == 1:
        probability = output[:, 0]
    elif output.ndim == 2 and output.shape[1] == 2:
        probability = output[:, 1]
    else:
        raise ValueError(f"Unsupported neural prediction output shape: {output.shape}")
    return np.asarray(probability, dtype=np.float64).reshape(-1)


def integrate_gradient_grid(
    path_gradients: np.ndarray,
    input_differences: np.ndarray,
    step_count: int,
    *,
    maximum_steps: int = MAX_STEPS,
) -> tuple[np.ndarray, np.ndarray]:
    """Integrate a nested Stage 14 gradient grid with the trapezoidal rule.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 151, 158
    Original stage: Stage 14
    Frozen artifacts generated: results/stage14_integrated_gradients/stage14_3b_ig_128_step_attributions.npz, results/stage14_integrated_gradients/stage14_4_ig_full_panel_attributions.npz
    Notes: Tests may supply synthetic gradients; this helper does not import TensorFlow, load models, or calculate gradients.
    """

    gradients = np.asarray(path_gradients, dtype=np.float64)
    differences = np.asarray(input_differences, dtype=np.float64)
    if maximum_steps % step_count != 0:
        raise ValueError(f"{step_count} does not divide maximum_steps={maximum_steps}")
    if gradients.ndim != 3 or gradients.shape[1] != maximum_steps + 1:
        raise ValueError("path_gradients must have shape (references, maximum_steps + 1, features)")
    if differences.shape != (gradients.shape[0], gradients.shape[2]):
        raise ValueError("input_differences shape does not match gradient references/features")
    stride = maximum_steps // step_count
    selected = gradients[:, np.arange(0, maximum_steps + 1, stride, dtype=np.int64), :]
    weights = np.ones(step_count + 1, dtype=np.float64)
    weights[[0, -1]] = 0.5
    mean_path_gradient = np.sum(selected * weights[None, :, None], axis=1) / float(step_count)
    per_reference = differences * mean_path_gradient
    return np.mean(per_reference, axis=0).astype(np.float64), per_reference.astype(np.float64)


def completeness_diagnostics(
    attribution: Sequence[float],
    input_logit: float,
    mean_baseline_logit: float,
) -> dict[str, float | bool]:
    """Evaluate Stage 14 absolute and normalized IG completeness errors.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 158
    Original stage: Stage 14
    Frozen artifacts generated: results/stage14_integrated_gradients/stage14_3b_ig_completeness_audit.csv
    Notes: Normalization denominator is max(abs(input_logit - mean_baseline_logit), 1.0).
    """

    target_difference = float(input_logit - mean_baseline_logit)
    signed_error = float(np.sum(np.asarray(attribution, dtype=np.float64)) - target_difference)
    absolute_error = abs(signed_error)
    normalized_error = absolute_error / max(abs(target_difference), 1.0)
    return {
        "signed_error": signed_error,
        "absolute_error": absolute_error,
        "normalized_error": normalized_error,
        "absolute_pass": absolute_error <= ABSOLUTE_COMPLETENESS_TOLERANCE,
        "normalized_pass": normalized_error <= NORMALIZED_COMPLETENESS_TOLERANCE,
        "completeness_pass": absolute_error <= ABSOLUTE_COMPLETENESS_TOLERANCE and normalized_error <= NORMALIZED_COMPLETENESS_TOLERANCE,
    }


def cosine_similarity(first: Sequence[float], second: Sequence[float]) -> float:
    """Calculate Stage 14 attribution cosine with its zero-vector convention.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 151, 152, 158
    Original stage: Stage 14
    Frozen artifacts generated: results/stage14_integrated_gradients/stage14_3b_ig_step_convergence.csv, results/stage14_integrated_gradients/stage14_4_ig_reference_diagnostics.csv
    Notes: Two near-zero vectors return 1.0; one near-zero vector returns 0.0.
    """

    left = np.asarray(first, dtype=np.float64)
    right = np.asarray(second, dtype=np.float64)
    denominator = np.linalg.norm(left) * np.linalg.norm(right)
    if denominator <= 1e-15:
        return 1.0 if np.linalg.norm(left) <= 1e-15 and np.linalg.norm(right) <= 1e-15 else 0.0
    return float(np.dot(left, right) / denominator)


def top_k_set(values: Sequence[float], k: int = TOP_K) -> set[int]:
    """Return the Stage 14 absolute-magnitude top-k feature set.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 151, 152, 158
    Original stage: Stage 14
    Frozen artifacts generated: results/stage14_integrated_gradients/stage14_3b_ig_step_convergence.csv, results/stage14_integrated_gradients/stage14_4b_ig_top10_term_reliability.csv
    Notes: Uses np.argsort(abs(values))[-k:] exactly.
    """

    return set(np.argsort(np.abs(np.asarray(values, dtype=np.float64)))[-k:].tolist())


def jaccard_similarity(first: Iterable[int], second: Iterable[int]) -> float:
    """Calculate Stage 14 top-k Jaccard with empty-union value 1.0.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 151, 152, 158
    Original stage: Stage 14
    Frozen artifacts generated: results/stage14_integrated_gradients/stage14_3b_ig_step_convergence.csv, results/stage14_integrated_gradients/stage14_4b_disagreement_baseline_sensitivity.csv
    Notes: Empty sets are treated as identical.
    """

    first_set, second_set = set(first), set(second)
    union = first_set | second_set
    return 1.0 if not union else float(len(first_set & second_set) / len(union))


def classify_reference_reliability(
    completeness_pass: bool,
    mean_cosine: float,
    minimum_cosine: float,
    mean_top10_jaccard: float,
    mean_top10_sign_agreement: float,
) -> str:
    """Apply Stage 14.4B case-level reference-reliability criteria.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 152
    Original stage: Stage 14
    Frozen artifacts generated: results/stage14_integrated_gradients/stage14_4b_ig_case_reliability.csv
    Notes: These thresholds are explicit study-specific presentation rules, not universal IG validity standards.
    """

    robust = completeness_pass and mean_cosine >= 0.65 and minimum_cosine >= 0.0 and mean_top10_jaccard >= 0.40 and mean_top10_sign_agreement >= 0.70
    if robust:
        return "Reference-robust"
    moderate = completeness_pass and mean_cosine >= 0.50 and mean_top10_jaccard >= 0.30 and mean_top10_sign_agreement >= 0.60
    return "Moderately reference-stable" if moderate else "Reference-sensitive"


def classify_feature_reference_stability(sign_consistency: float) -> str:
    """Apply Stage 14 feature-direction stability thresholds.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 152
    Original stage: Stage 14
    Frozen artifacts generated: results/stage14_integrated_gradients/stage14_4b_ig_top10_term_reliability.csv
    Notes: Reference-stable requires >=0.75 and moderately stable requires >=0.65.
    """

    if sign_consistency >= 0.75:
        return "Reference-stable direction"
    if sign_consistency >= 0.65:
        return "Moderately stable direction"
    return "Reference-sensitive direction"


def classify_baseline_agreement(signed_cosine: float, top10_jaccard: float, top10_sign_agreement: float) -> str:
    """Apply the Stage 14 alternative-baseline agreement classification.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 152
    Original stage: Stage 14
    Frozen artifacts generated: results/stage14_integrated_gradients/stage14_4b_disagreement_baseline_sensitivity.csv
    Notes: Strong thresholds are 0.80/0.50/0.80; moderate thresholds are 0.60/0.30/0.60.
    """

    if signed_cosine >= 0.80 and top10_jaccard >= 0.50 and top10_sign_agreement >= 0.80:
        return "Strong baseline agreement"
    if signed_cosine >= 0.60 and top10_jaccard >= 0.30 and top10_sign_agreement >= 0.60:
        return "Moderate baseline agreement"
    return "Weak baseline agreement"
