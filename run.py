#!/usr/bin/env python3
"""Обычный запуск: python run.py"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mapsparseruzao.bootstrap import preflight  # noqa: E402
from mapsparseruzao.cli import main  # noqa: E402


if __name__ == "__main__":
    problem = preflight()
    if problem:
        print(problem, file=sys.stderr)
        sys.exit(2)
    main()
