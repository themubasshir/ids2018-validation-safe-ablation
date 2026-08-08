# Auto-frozen by Stage 19.2B.
# Do not modify during Stage 19 training.

import numpy as np


BASE_FEATURE_COUNT = 78
TOKEN_FEATURE_COUNT = 80

WARMUP_SECONDS = 1200

FINE_TOKEN_SECONDS = 1
FINE_TOKEN_COUNT = 60

MEDIUM_TOKEN_SECONDS = 15
MEDIUM_TOKEN_COUNT = 20

COARSE_TOKEN_SECONDS = 60
COARSE_TOKEN_COUNT = 20


def standardize_base(
    feature_mean_raw,
    impute_mean,
    scale,
):
    """
    TRAIN-frozen mean imputation and z-standardization
    of the 78 second-level numeric channels.
    """

    x = np.asarray(
        feature_mean_raw,
        dtype=np.float64,
    )

    mu = np.asarray(
        impute_mean,
        dtype=np.float64,
    )

    sigma = np.asarray(
        scale,
        dtype=np.float64,
    )

    if x.ndim != 2:
        raise ValueError("feature_mean_raw must be 2-D")

    if x.shape[1] != BASE_FEATURE_COUNT:
        raise ValueError("unexpected base feature count")

    if mu.shape != (BASE_FEATURE_COUNT,):
        raise ValueError("unexpected impute_mean shape")

    if sigma.shape != (BASE_FEATURE_COUNT,):
        raise ValueError("unexpected scale shape")

    if not np.all(sigma > 0):
        raise ValueError("scale must be strictly positive")

    finite = np.isfinite(x)

    imputed = np.where(
        finite,
        x,
        mu,
    )

    standardized = (
        imputed
        - mu
    ) / sigma

    if not np.all(
        np.isfinite(
            standardized
        )
    ):
        raise ValueError(
            "nonfinite standardized values"
        )

    return standardized.astype(
        np.float32
    )


def _append_activity(
    base_tokens,
    bin_flow_count,
):
    """
    Append:
      log1p(total flow count in token)
      occupancy indicator
    """

    base_tokens = np.asarray(
        base_tokens,
        dtype=np.float32,
    )

    bin_flow_count = np.asarray(
        bin_flow_count,
        dtype=np.float64,
    )

    log_count = np.log1p(
        bin_flow_count
    ).astype(
        np.float32
    )

    occupied = (
        bin_flow_count
        > 0
    ).astype(
        np.float32
    )

    return np.concatenate(
        [
            base_tokens,
            log_count[:, None],
            occupied[:, None],
        ],
        axis=1,
    ).astype(
        np.float32
    )


def construct_multiscale(
    base_standardized,
    flow_count,
    target_local_index,
):
    """
    Construct one causal MTemporal-IDS sample.

    Every branch terminates at target_local_index.

    Fine:
      [t-59, ..., t]

    Medium:
      [t-299, ..., t]
      reshaped into 20 consecutive 15-second bins.

    Coarse:
      [t-1199, ..., t]
      reshaped into 20 consecutive 60-second bins.

    No future second is accessed.
    """

    base = np.asarray(
        base_standardized,
        dtype=np.float32,
    )

    count = np.asarray(
        flow_count,
        dtype=np.int64,
    )

    t = int(
        target_local_index
    )

    if base.ndim != 2:
        raise ValueError(
            "base_standardized must be 2-D"
        )

    if base.shape[1] != BASE_FEATURE_COUNT:
        raise ValueError(
            "unexpected base feature count"
        )

    if count.shape != (
        base.shape[0],
    ):
        raise ValueError(
            "flow_count length mismatch"
        )

    if t < WARMUP_SECONDS:
        raise ValueError(
            "target precedes frozen 20-minute warmup"
        )

    if t >= base.shape[0]:
        raise ValueError(
            "target exceeds source-day span"
        )


    # --------------------------------------------------------
    # Fine branch
    # --------------------------------------------------------

    fine_start = (
        t
        - FINE_TOKEN_COUNT
        + 1
    )

    fine_base = base[
        fine_start:
        t + 1
    ]

    fine_count = count[
        fine_start:
        t + 1
    ]

    if fine_base.shape != (
        FINE_TOKEN_COUNT,
        BASE_FEATURE_COUNT,
    ):
        raise RuntimeError(
            "invalid fine shape"
        )

    fine = _append_activity(
        fine_base,
        fine_count,
    )


    # --------------------------------------------------------
    # Medium branch
    # --------------------------------------------------------

    medium_start = (
        t
        - (
            MEDIUM_TOKEN_SECONDS
            * MEDIUM_TOKEN_COUNT
        )
        + 1
    )

    medium_base_seconds = base[
        medium_start:
        t + 1
    ]

    medium_count_seconds = count[
        medium_start:
        t + 1
    ]


    medium_base = (
        medium_base_seconds
        .reshape(
            MEDIUM_TOKEN_COUNT,
            MEDIUM_TOKEN_SECONDS,
            BASE_FEATURE_COUNT,
        )
        .mean(
            axis=1,
            dtype=np.float32,
        )
    )


    medium_count = (
        medium_count_seconds
        .reshape(
            MEDIUM_TOKEN_COUNT,
            MEDIUM_TOKEN_SECONDS,
        )
        .sum(
            axis=1,
            dtype=np.int64,
        )
    )


    medium = _append_activity(
        medium_base,
        medium_count,
    )


    # --------------------------------------------------------
    # Coarse branch
    # --------------------------------------------------------

    coarse_start = (
        t
        - (
            COARSE_TOKEN_SECONDS
            * COARSE_TOKEN_COUNT
        )
        + 1
    )

    coarse_base_seconds = base[
        coarse_start:
        t + 1
    ]

    coarse_count_seconds = count[
        coarse_start:
        t + 1
    ]


    coarse_base = (
        coarse_base_seconds
        .reshape(
            COARSE_TOKEN_COUNT,
            COARSE_TOKEN_SECONDS,
            BASE_FEATURE_COUNT,
        )
        .mean(
            axis=1,
            dtype=np.float32,
        )
    )


    coarse_count = (
        coarse_count_seconds
        .reshape(
            COARSE_TOKEN_COUNT,
            COARSE_TOKEN_SECONDS,
        )
        .sum(
            axis=1,
            dtype=np.int64,
        )
    )


    coarse = _append_activity(
        coarse_base,
        coarse_count,
    )


    if fine.shape != (
        60,
        TOKEN_FEATURE_COUNT,
    ):
        raise RuntimeError(
            "invalid fine token tensor"
        )

    if medium.shape != (
        20,
        TOKEN_FEATURE_COUNT,
    ):
        raise RuntimeError(
            "invalid medium token tensor"
        )

    if coarse.shape != (
        20,
        TOKEN_FEATURE_COUNT,
    ):
        raise RuntimeError(
            "invalid coarse token tensor"
        )


    return (
        fine,
        medium,
        coarse,
    )


def construct_fine_only(
    base_standardized,
    flow_count,
    target_local_index,
):
    """
    Frozen SingleScaleTemporalTransformer control input.
    """

    fine, _, _ = construct_multiscale(
        base_standardized,
        flow_count,
        target_local_index,
    )

    return fine
