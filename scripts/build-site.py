#!/usr/bin/env python3
"""Production build: use existing HTML sources and refresh derived resources."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
for script in ('build-service-cases.py', 'build-ai-search.py', 'build-ai-catalog.py',
               'check-ai-search.py', 'check-geo-seo.py'):
    subprocess.run([sys.executable, str(ROOT / 'scripts' / script)], cwd=ROOT, check=True)
