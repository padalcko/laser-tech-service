#!/usr/bin/env python3
"""Generate EN commercial prices from explicitly bound PLN HTML and a pinned NBP rate."""
import argparse
import re
from eur_pricing import ROOT, config, bindings, update, amount

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check', action='store_true')
args = parser.parse_args()
c = config()
data = bindings()
stale = []
for relative, refs in data['pages'].items():
    path = ROOT / relative
    source = path.read_text()
    updated = update(source, refs, c)
    if relative == 'en/pricing/index.html':
        tariff = amount(data['travel_tariff'], c)
        updated = re.sub(r'data-eur-km="\d+"', f'data-eur-km="{tariff}"', updated)
    if source != updated:
        stale.append(relative)
        if not args.check: path.write_text(updated)
print(f'EN commercial prices: {sum(len(x) for x in data["pages"].values())} occurrences, {len(data["pages"])} pages; stale: {len(stale)}')
if args.check and stale: raise SystemExit(1)
