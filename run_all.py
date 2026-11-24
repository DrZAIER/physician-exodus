"""Run the full analysis pipeline, including the supplementary flow diagram."""

import subprocess
import sys
from pathlib import Path

from src.analysis import main

ROOT = Path(__file__).resolve().parent


def run() -> None:
    main()
    # The flow diagram is standalone; run it so one command rebuilds every
    # table and figure cited in the manuscript and supplement.
    subprocess.run([sys.executable, str(ROOT / "src" / "fig_flow.py")],
                   cwd=ROOT, check=True)


if __name__ == "__main__":
    run()
