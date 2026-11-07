#!/usr/bin/env python3
"""Production build: use existing HTML sources and refresh derived resources."""
from pathlib import Path
import subprocess
import sys
import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

ROOT = Path(__file__).resolve().parents[1]
for script in ('build-about.py', 'check-site-locales.py', 'build-eur-prices.py', 'build-language-switcher.py', 'check-language-switcher.py', 'build-service-menu.py', 'build-corporate-menu.py', 'build-service-cases.py', 'build-partners.py', 'build-blog-reading-times.py', 'build-ai-search.py', 'build-ai-catalog.py', 'build-performance-assets.py --html-only',
               'check-ai-search.py', 'check-geo-seo.py', 'check-eur-prices.py'):
    command = script.split()
    subprocess.run([sys.executable, str(ROOT / 'scripts' / command[0]), *command[1:]], cwd=ROOT, check=True)
