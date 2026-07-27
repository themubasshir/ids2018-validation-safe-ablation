# Dataset

This experiment uses the processed binary CSE-CIC-IDS2018 dataset referenced in the archive metadata as `merged_balanced_ids2018_safe.csv`.

- Source name: CSE-CIC-IDS2018.
- Processed dataset path in the archived Kaggle environment: `/kaggle/input/datasets/jmmubasshirrahman/ids2018-balanced-binary-dataset/merged_balanced_ids2018_safe.csv`.
- Total records: 300,928.
- Predictors: 78.
- Dataset columns in metadata: 80.
- Excluded columns: `Label` and `binary_label`.
- Class distribution: 180,000 benign records and 120,928 attack records.

The raw and processed dataset files are not included here. Users should obtain CSE-CIC-IDS2018 under its applicable terms and supply the processed binary dataset locally when rerunning training or evaluation. A convenient local convention is:

```text
data/raw/merged_balanced_ids2018_safe.csv
```

That path is ignored by Git to avoid accidental redistribution.
