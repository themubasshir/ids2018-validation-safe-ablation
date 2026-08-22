"""Exact Stage 2 classical and boosting baseline constructors."""

from __future__ import annotations

from typing import Any


def build_baseline_models(
    *,
    random_state: int = 42,
    xgb_device_parameters: dict[str, Any] | None = None,
    xgb_device_label: str = "CPU",
    lightgbm_backend: str = "cpu",
    lightgbm_device_label: str = "CPU",
    catboost_task_type: str = "CPU",
    catboost_device_label: str = "CPU",
) -> list[dict[str, Any]]:
    """Construct the 12 notebook baseline estimators without fitting them.

    Source notebook: notebooks/archive/stage01_to_stage20_original_kaggle_notebook.ipynb
    Original physical cell(s): 94
    Original stage: Stage 2
    Frozen artifacts generated: metadata/baseline_model_configurations.json, results/baseline/baseline12_validation_results.csv
    Notes: Imports are lazy; accelerator detection remains an explicit caller input.
    """

    from catboost import CatBoostClassifier
    from lightgbm import LGBMClassifier
    from sklearn.ensemble import (
        AdaBoostClassifier,
        ExtraTreesClassifier,
        GradientBoostingClassifier,
        RandomForestClassifier,
    )
    from sklearn.linear_model import LogisticRegression
    from sklearn.naive_bayes import GaussianNB
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import LinearSVC
    from sklearn.tree import DecisionTreeClassifier
    from xgboost import XGBClassifier

    xgb_device_parameters = dict(xgb_device_parameters or {"tree_method": "hist"})
    return [
        {"name": "Logistic Regression", "model": LogisticRegression(solver="lbfgs", max_iter=1_000, random_state=random_state), "input": "scaled", "device": "CPU", "prediction_method": "predict"},
        {"name": "Naive Bayes", "model": GaussianNB(), "input": "scaled", "device": "CPU", "prediction_method": "predict"},
        {"name": "KNN", "model": KNeighborsClassifier(n_neighbors=5, weights="uniform", n_jobs=-1), "input": "scaled", "device": "CPU", "prediction_method": "predict"},
        {"name": "Linear SVM", "model": LinearSVC(C=1.0, max_iter=10_000, random_state=random_state), "input": "scaled", "device": "CPU", "prediction_method": "predict"},
        {"name": "Decision Tree", "model": DecisionTreeClassifier(random_state=random_state), "input": "raw", "device": "CPU", "prediction_method": "predict"},
        {"name": "Random Forest", "model": RandomForestClassifier(n_estimators=100, random_state=random_state, n_jobs=-1), "input": "raw", "device": "CPU", "prediction_method": "predict"},
        {"name": "Extra Trees", "model": ExtraTreesClassifier(n_estimators=100, random_state=random_state, n_jobs=-1), "input": "raw", "device": "CPU", "prediction_method": "predict"},
        {"name": "AdaBoost", "model": AdaBoostClassifier(n_estimators=50, learning_rate=1.0, random_state=random_state), "input": "raw", "device": "CPU", "prediction_method": "predict"},
        {"name": "Gradient Boosting", "model": GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=random_state), "input": "raw", "device": "CPU", "prediction_method": "predict"},
        {"name": "XGBoost", "model": XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.3, subsample=1.0, colsample_bytree=1.0, objective="binary:logistic", eval_metric="logloss", random_state=random_state, n_jobs=-1, **xgb_device_parameters), "input": "raw", "device": xgb_device_label, "prediction_method": "predict"},
        {"name": "LightGBM", "model": LGBMClassifier(n_estimators=100, learning_rate=0.1, num_leaves=31, objective="binary", device_type=lightgbm_backend, random_state=random_state, n_jobs=-1, verbosity=-1), "input": "raw", "device": lightgbm_device_label, "prediction_method": "predict"},
        {"name": "CatBoost", "model": CatBoostClassifier(iterations=300, depth=6, learning_rate=0.1, loss_function="Logloss", eval_metric="F1", task_type=catboost_task_type, devices="0" if catboost_task_type == "GPU" else None, random_seed=random_state, verbose=False, allow_writing_files=False), "input": "raw", "device": catboost_device_label, "prediction_method": "predict"},
    ]
