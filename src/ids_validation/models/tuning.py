"""Stage 3 search spaces, candidate grids, and lazy estimator constructors."""

from __future__ import annotations

from typing import Any


RANDOM_STATE = 42
CV_FOLDS = 3
N_ITERATIONS = 15
MAX_EPOCHS = 50
PATIENCE = 5
INTERNAL_VALIDATION_SIZE = 0.15

XGBOOST_PARAMETER_SPACE = {
    "n_estimators": [200, 300, 500, 700],
    "max_depth": [4, 6, 8, 10],
    "learning_rate": [0.03, 0.05, 0.10],
    "min_child_weight": [1, 3, 5],
    "subsample": [0.80, 0.90, 1.00],
    "colsample_bytree": [0.80, 0.90, 1.00],
    "gamma": [0.0, 0.1, 0.3],
    "reg_alpha": [0.0, 0.1, 1.0],
    "reg_lambda": [1.0, 5.0, 10.0],
}

LIGHTGBM_PARAMETER_SPACE = {
    "n_estimators": [200, 400, 700],
    "learning_rate": [0.03, 0.05, 0.10],
    "num_leaves": [31, 63, 127],
    "max_depth": [-1, 15, 30],
    "min_child_samples": [10, 20, 40],
    "subsample": [0.80, 0.90, 1.00],
    "colsample_bytree": [0.80, 0.90, 1.00],
    "reg_alpha": [0.0, 0.1, 1.0],
    "reg_lambda": [0.0, 1.0, 5.0],
}

CATBOOST_PARAMETER_SPACE = {
    "iterations": [300, 500, 700],
    "learning_rate": [0.03, 0.05, 0.10],
    "depth": [6, 8, 10],
    "l2_leaf_reg": [3, 5, 7],
    "random_strength": [0.5, 1.0, 2.0],
    "border_count": [64, 128, 254],
}

MLP_CANDIDATES = [
    {"Candidate": "MLP-01", "Hidden Layers": [128, 64], "Dropout": 0.20, "Learning Rate": 0.001, "Batch Size": 1024},
    {"Candidate": "MLP-02", "Hidden Layers": [256, 128], "Dropout": 0.20, "Learning Rate": 0.0005, "Batch Size": 1024},
    {"Candidate": "MLP-03", "Hidden Layers": [256, 128, 64], "Dropout": 0.20, "Learning Rate": 0.0005, "Batch Size": 1024},
    {"Candidate": "MLP-04", "Hidden Layers": [256, 128, 64], "Dropout": 0.30, "Learning Rate": 0.001, "Batch Size": 512},
    {"Candidate": "MLP-05", "Hidden Layers": [512, 256, 128], "Dropout": 0.30, "Learning Rate": 0.0005, "Batch Size": 1024},
    {"Candidate": "MLP-06", "Hidden Layers": [512, 256, 128, 64], "Dropout": 0.30, "Learning Rate": 0.0003, "Batch Size": 1024},
]

CNN_CANDIDATES = [
    {"Candidate": "CNN-01", "Filters": [64, 128], "Kernel Size": 3, "Dropout": 0.20, "Dense Units": 64, "Learning Rate": 0.001, "Batch Size": 1024},
    {"Candidate": "CNN-02", "Filters": [128, 256], "Kernel Size": 3, "Dropout": 0.30, "Dense Units": 128, "Learning Rate": 0.0005, "Batch Size": 1024},
    {"Candidate": "CNN-03", "Filters": [128, 256], "Kernel Size": 5, "Dropout": 0.30, "Dense Units": 128, "Learning Rate": 0.0005, "Batch Size": 512},
    {"Candidate": "CNN-04", "Filters": [64, 128, 256], "Kernel Size": 3, "Dropout": 0.30, "Dense Units": 128, "Learning Rate": 0.0005, "Batch Size": 1024},
    {"Candidate": "CNN-05", "Filters": [128, 256, 256], "Kernel Size": 5, "Dropout": 0.40, "Dense Units": 128, "Learning Rate": 0.0003, "Batch Size": 512},
    {"Candidate": "CNN-06", "Filters": [256, 256], "Kernel Size": 5, "Dropout": 0.30, "Dense Units": 256, "Learning Rate": 0.0003, "Batch Size": 1024},
]


def build_xgboost_estimator(device_parameters: dict[str, Any] | None = None) -> Any:
    """Construct the Stage 3 XGBoost search estimator without fitting.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 96
    Original stage: Stage 3
    Frozen artifacts generated: results/tuning/xgboost/xgboost_best_parameters.json
    Notes: Runtime GPU probing selected version-specific device parameters.
    """

    from xgboost import XGBClassifier

    return XGBClassifier(objective="binary:logistic", eval_metric="logloss", random_state=RANDOM_STATE, n_jobs=1, verbosity=0, **dict(device_parameters or {"tree_method": "hist"}))


def build_lightgbm_estimator(backend: str = "cpu") -> Any:
    """Construct the Stage 3 LightGBM search estimator without fitting.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 97
    Original stage: Stage 3
    Frozen artifacts generated: results/tuning/lightgbm/lightgbm_best_parameters.json
    Notes: The notebook probes gpu then cuda and otherwise uses cpu.
    """

    from lightgbm import LGBMClassifier

    return LGBMClassifier(objective="binary", device_type=backend, subsample_freq=1, random_state=RANDOM_STATE, n_jobs=-1, verbosity=-1)


def build_catboost_estimator(task_type: str = "CPU") -> Any:
    """Construct the Stage 3 CatBoost search estimator without fitting.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 98
    Original stage: Stage 3
    Frozen artifacts generated: results/tuning/catboost/catboost_best_parameters.json
    Notes: devices='0' is added only when the runtime probe selects GPU.
    """

    from catboost import CatBoostClassifier

    parameters: dict[str, Any] = {"loss_function": "Logloss", "eval_metric": "F1", "task_type": task_type, "random_seed": RANDOM_STATE, "verbose": False, "allow_writing_files": False}
    if task_type == "GPU":
        parameters["devices"] = "0"
    return CatBoostClassifier(**parameters)


def build_randomized_search(estimator: Any, parameter_space: dict[str, list[Any]]) -> Any:
    """Construct the exact Stage 3 three-fold, 15-candidate search object.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 96, 97, 98
    Original stage: Stage 3
    Frozen artifacts generated: results/tuning/*/*_random_search_results.csv
    Notes: n_jobs=1 and pre_dispatch=1 intentionally preserve GPU-safe scheduling.
    """

    from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold

    cv_strategy = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)
    return RandomizedSearchCV(estimator=estimator, param_distributions=parameter_space, n_iter=N_ITERATIONS, scoring="f1", cv=cv_strategy, refit=True, n_jobs=1, random_state=RANDOM_STATE, verbose=2, return_train_score=False, error_score="raise", pre_dispatch=1)
