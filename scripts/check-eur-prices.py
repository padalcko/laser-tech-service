#!/usr/bin/env python3
"""Audit explicit commercial bindings, protected PLN/history and generated resources."""
import json
import re
from decimal import Decimal, ROUND_CEILING
from pathlib import Path
from eur_pricing import ROOT, config, bindings, source_amount, amount, convert, render, update, EN_TOKEN, PL_TOKEN

c, b = config(), bindings()
assert c['nbp']['effective_date'] <= c['generated_date']
assert c['nbp']['table_number'] == '206/A/NBP/2026'
assert c['nbp']['effective_date'] == '2026-10-22' and c['nbp']['rate'] == '4.3685'
count = 0
for relative, refs in b['pages'].items():
    s = (ROOT / relative).read_text()
    tokens = list(EN_TOKEN.finditer(s))
    assert len(tokens) == len(refs), relative
    assert update(s, refs, c) == s, relative
    assert update(update(s, refs, c), refs, c) == s, 'Double conversion'
    for token, bound in zip(tokens, refs):
        assert token[0] == render(bound, c), (relative, token[0])
        for ref in bound:
            expected = int((source_amount(ref) * Decimal('1.20') / Decimal(c['nbp']['rate'])).to_integral_value(rounding=ROUND_CEILING))
            if ref.get('multiplier'): expected *= int(ref['multiplier'])
            assert amount(ref, c) == expected
        count += 1
    assert not re.search(r'\bPLN\b|\bzł\b', s), relative
    md = (ROOT / relative).with_suffix('.md').read_text()
    for token in EN_TOKEN.findall(md):
        assert ('EUR '+token[0]) in s, (relative,token)
    assert update(s, refs, c) == s
# Zero remains zero, and ceilings apply to both range endpoints.
assert convert('0') == 0 and convert('700') == 193 and convert('1000') == 275
assert amount(b['travel_tariff']) == 1
assert 'data-eur-km="1"' in (ROOT/'en/pricing/index.html').read_text()
assert '100 km = EUR 100' in (ROOT/'en/pricing/index.html').read_text()
protected = json.loads((ROOT/'scripts/price-baseline.json').read_text())
for relative, expected in protected.items():
    s = (ROOT/relative).read_text()
    pattern = EN_TOKEN if relative.startswith('en/') else PL_TOKEN
    assert [m[0] for m in pattern.finditer(s)] == expected, ('Protected prices changed',relative)
for path in (ROOT/'en').rglob('index.html'):
    if re.search(r'\bPLN\b|\bzł\b',path.read_text()):
        assert str(path.relative_to(ROOT)) in b['historical_pages'],path
catalog = json.loads((ROOT/'ai-catalog.json').read_text())
for record in catalog['services']:
    pl,en = record['localizations']['pl']['starting_price'],record['localizations']['en']['starting_price']
    if pl:
        assert en['currency']=='EUR' and en['amount']==convert(str(pl['amount'])),record['id']
    else: assert en is None
print(f'PASS: {count} commercial occurrences / {len(b["pages"])} pages; Decimal formula, ranges, travel tariff, idempotence, protected PL/RU and historical prices, catalog and Markdown')
