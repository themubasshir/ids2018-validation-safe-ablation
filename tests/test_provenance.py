from __future__ import annotations

import inspect
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ids_validation.common.provenance import has_required_provenance_fields
from ids_validation.data import duplicate_safe_split, graph_snapshots, ids2018, temporal_bins
from ids_validation.evaluation import attention, attack_categories, bootstrap, calibration, metrics, multiseed, operating_cost, thresholds
from ids_validation.explainability import integrated_gradients, lime_analysis, local_agreement, shap_analysis
from ids_validation.models import baselines, classical, ft_transformer, graph_models, neural, temporal_models, tuning
from ids_validation.stages.stage07 import publication
from ids_validation.stages.stage20.directed_s4 import signature
from ids_validation.stages.stage20.evaluation import operating_points as stage20_operating_points
from ids_validation.stages.stage20.extractor_forensics import flags
from ids_validation.stages.stage20.packet_representation import encoder, geometry
from ids_validation.stages.stage20.reconstruction import transitions
from ids_validation.stages.stage22 import registry as stage22_registry
from ids_validation.stages.stage23 import registry as stage23_registry
from ids_validation.stages.stage24 import registry as stage24_registry


class ExtractedFunctionProvenanceTests(unittest.TestCase):
    def test_all_public_extracted_functions_have_required_fields(self) -> None:
        modules = (
            ids2018,
            metrics,
            thresholds,
            baselines,
            neural,
            tuning,
            shap_analysis,
            publication,
            bootstrap,
            calibration,
            operating_cost,
            attack_categories,
            multiseed,
            lime_analysis,
            local_agreement,
            integrated_gradients,
            duplicate_safe_split,
            ft_transformer,
            classical,
            attention,
            graph_snapshots,
            graph_models,
            temporal_bins,
            temporal_models,
            signature,
            flags,
            transitions,
            geometry,
            encoder,
            stage20_operating_points,
            stage22_registry,
            stage23_registry,
            stage24_registry,
        )
        missing = []
        for module in modules:
            for name, function in inspect.getmembers(module, inspect.isfunction):
                if function.__module__ == module.__name__ and not name.startswith("_"):
                    if not has_required_provenance_fields(inspect.getdoc(function)):
                        missing.append(f"{module.__name__}.{name}")
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
