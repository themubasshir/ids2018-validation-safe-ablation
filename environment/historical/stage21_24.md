# Stage21–24 Environments

- Stage21 proves Python 3.12.13, NumPy 2.4.6 and PyTorch 2.10.0+cu126 with
  CUDA 12.6/cuDNN 9.1.0.2 on a Tesla T4.
- Stage22 proves the learner/package backends, but Python version and GPU model
  remain `VERSION_NOT_PROVEN`.
- Stage23 proves NumPy/pandas/scikit-learn, LightGBM, XGBoost and SHAP, but
  Python version and GPU model remain `VERSION_NOT_PROVEN`.
- Stage24 has its own Python 3.12.13 and two-Tesla-T4 bootstrap receipt with
  the package versions recorded in `ENVIRONMENT_REGISTRY.csv`.

None of these records may be inherited by another stage without direct
evidence.
