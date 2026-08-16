# Stage21-XAI1A-R1 — Exact XAI Preflight

## Status

**EXACT PREFLIGHT DURABLY SEALED BEFORE ANY ATTRIBUTION**

The initial XAI1A verification used the Stage21 canonical-state serialization
for both architectures.

That verification rule was inappropriate for the immutable Stage20 comparator,
whose original Stage20-1E2 training execution used a different historical
canonical-state serialization.

No model, checkpoint, architecture, cohort, attribution method, threshold, or
scientific result changed.

## CNN identity

- checkpoint SHA256: `3ebc71e579dc8e0e545981b2d60eea643148fe53e0902f8df8e47556243ad30b`
- canonical state SHA256: `ae9c913b13db62ab933198dd7721f0d1826b26a55773e3b560dc735cbb8c8092`
- parameters: **93,025**
- strict state-dict loading: **PASS**
- canonicalization: **historical Stage20-1E2**

The Stage20 hash serializes, for every sorted state key:

1. UTF-8 parameter name
2. ASCII NumPy dtype
3. compact JSON tensor shape
4. C-order tensor bytes

Each piece is preceded by an unsigned 8-byte big-endian byte-length prefix.

## ViT identity

- checkpoint SHA256: `221e9c805fb663acacf2f0f2ca95dba7cb4b2ec4c4de5a3650cf4adeb99b5ef8`
- canonical state SHA256: `9da47df6cd5c821eef3d2c8a501296cd6070b835c719999f572f3dec2d560771`
- parameters: **91,969**
- strict state-dict loading: **PASS**
- canonicalization: **Stage21**

## Scientific boundary

- XAI protocol changed: **NO**
- model weights changed: **NO**
- model forwards: **0**
- gradient passes: **0**
- Integrated Gradients runs: **0**
- attributions observed: **NO**
- threshold search/reselection: **NO**
- retraining: **NO**
- optimizer steps: **0**

The locked Stage21-XAI0 protocol remains unchanged.
