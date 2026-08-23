# Stage08–14 Analysis Environments

These stages do not share one universal runtime. Stage08 and Stage09 have
separate complete analysis receipts. Stage12–14 have stage-specific partial or
complete package evidence. Stages10–11 remain largely `VERSION_NOT_PROVEN`.

- Stage08: Python 3.12.13, NumPy 2.4.6, pandas 2.3.3, scikit-learn 1.6.1,
  Matplotlib 3.10.0 and Joblib 1.5.3.
- Stage09: Python 3.12.13, NumPy 2.4.6, pandas 2.3.3, SciPy 1.16.3,
  Matplotlib 3.10.0 and Joblib 1.5.3.
- Stage12: core learner versions are proven; Joblib, Matplotlib and tar are
  unproven.
- Stage13: LIME 0.2.0.1 and the core learner stack are proven; SHAP, SciPy and
  Matplotlib are unproven.
- Stage14: TensorFlow 2.19.0 is proven; standalone Keras, scikit-learn,
  Joblib and Matplotlib are unproven.

See `ENVIRONMENT_REGISTRY.csv` and the stage configs for exact evidence scope.
