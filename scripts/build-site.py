#!/usr/bin/env python3
"""Production build: use existing HTML sources and refresh derived resources."""
from pathlib import Path
import subprocess
import sys
import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

ROOT = Path(__file__).resolve().parents[1]
for script in ('check-site-locales.py', 'build-eur-prices.py', 'build-language-switcher.py', 'check-language-switcher.py', 'build-service-cases.py', 'build-ai-search.py', 'build-ai-catalog.py',
               'check-ai-search.py', 'check-geo-seo.py'):
    subprocess.run([sys.executable, str(ROOT / 'scripts' / script)], cwd=ROOT, check=True)
