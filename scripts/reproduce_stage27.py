"""Safety-gated Stage 27 canonical-source entry point."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ids_validation.common.protocol_cli import run_protocol_cli
if __name__ == "__main__":
    raise SystemExit(run_protocol_cli(27))
