from __future__ import annotations

import inspect
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ids_validation.common.provenance import has_required_provenance_fields
from ids_validation.data import ids2018
from ids_validation.evaluation import metrics, thresholds
from ids_validation.models import baselines, neural, tuning


class ExtractedFunctionProvenanceTests(unittest.TestCase):
    def test_all_public_extracted_functions_have_required_fields(self) -> None:
        modules = (ids2018, metrics, thresholds, baselines, neural, tuning)
        missing = []
        for module in modules:
            for name, function in inspect.getmembers(module, inspect.isfunction):
                if function.__module__ == module.__name__ and not name.startswith("_"):
                    if not has_required_provenance_fields(inspect.getdoc(function)):
                        missing.append(f"{module.__name__}.{name}")
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
