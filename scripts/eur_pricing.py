"""Pinned NBP conversion; PLN HTML remains authoritative. No network at build time."""
import json
import re
from decimal import Decimal, ROUND_CEILING
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PL_NUMBER = r'(?:\d{1,3}(?:[ \u00a0]\d{3})+|\d+)(?:,\d{1,2})?'
PL_TOKEN = re.compile(r'(' + PL_NUMBER + r')(?:[–−-](' + PL_NUMBER + r'))?\s*zł')
EN_NUMBER = r'(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d{1,2})?'
EN_TOKEN = re.compile(r'\b(?:PLN|EUR)\s+(' + EN_NUMBER + r')(?:[–−-](' + EN_NUMBER + r'))?')

def config():
    c = json.loads((ROOT / 'scripts/eur-pricing.json').read_text())
    assert c['nbp']['table'] == 'A' and c['nbp']['code'] == 'EUR'
    assert Decimal(c['nbp']['rate']) > 0 and Decimal(c['markup']) == Decimal('0.20')
    return c

def convert(pln, c=None):
    c = c or config()
    return int((Decimal(pln) * (Decimal('1') + Decimal(c['markup'])) / Decimal(c['nbp']['rate'])).to_integral_value(rounding=ROUND_CEILING))

def source_amount(ref):
    matches = list(PL_TOKEN.finditer((ROOT / ref['file']).read_text()))
    value = matches[ref['token']].group(ref['endpoint'])
    assert value is not None, ref
    return Decimal(value.replace(' ', '').replace('\u00a0', '').replace(',', '.'))

def amount(ref, c=None):
    value = source_amount(ref)
    if ref.get('multiplier'):
        # The approved travel tariff is rounded first, then multiplied by distance.
        return convert(value, c) * int(ref['multiplier'])
    return convert(value, c)

def render(refs, c=None):
    return 'EUR ' + '–'.join(format(amount(ref, c), ',') for ref in refs)

def bindings():
    return json.loads((ROOT / 'scripts/en-price-bindings.json').read_text())

def update(source, refs, c):
    matches = list(EN_TOKEN.finditer(source))
    assert len(matches) == len(refs), 'Price occurrence count changed: review the explicit source bindings'
    result = source
    for match, bound in reversed(list(zip(matches, refs))):
        result = result[:match.start()] + render(bound, c) + result[match.end():]
    return result
