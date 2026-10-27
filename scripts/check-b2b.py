#!/usr/bin/env python3
"""Validate B2B page content, locale pairs, schema and existing form contract."""
import importlib.util
import json
from pathlib import Path
import site_locales as locales
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ai',R/'scripts/build-ai-search.py');ai=importlib.util.module_from_spec(spec);spec.loader.exec_module(ai)
g=next(g for g in locales.load()['pages'] if g['id']=='uslugi:serwis-dla-sieci-salonow')
pages={p['canonical']:p for p in ai.discover()}
for lang,url in locales.published(g).items():
 p=pages[ai.BASE+url];main=next(p['tree'].all('main'));assert p['alternates']==locales.alternates(g,ai.BASE)
 assert len(list(main.all('h1')))==1
 assert len([n for n in main.all() if n.has('faq__item')])==6
 assert len(list(next(main.all('ol')).all('li')))==3
 form=next(main.all('form'));assert 'data-b2b-form' in form.attrs
 fields={n.attrs.get('name'):n for n in form.all() if n.tag in ('input','select','textarea')}
 for name in ['salonName','fullName','phone','salonCount','consent']:assert 'required' in fields[name].attrs
 for name in ['deviceName','problemDescription']:assert 'required' not in fields[name].attrs
 assert [n.attrs.get('value') for n in fields['salonCount'].all('option')]==['','1','2-5','6-10','10+']
 assert fields['serviceType'].attrs['value']=='b2b-service'
 assert fields['source'].attrs['value']==lang+'-b2b-service'
 assert fields['companyWebsite'].attrs['tabindex']=='-1'
 schemas=list(ai.nodes(p['schemas'])) if hasattr(ai,'nodes') else p['schemas'][0]['@graph']
 service=next(n for n in schemas if n.get('@type')=='Service');assert service['provider']['@id']==ai.BASE+'/#organization'
 assert not any(n.get('@type')=='FAQPage' for n in schemas)
 if lang=='pl':
  for phrase in ['serwis laserów','naprawa laserów','regeneracja laserów','serwis urządzeń kosmetycznych','serwis urządzeń kosmetologicznych','obsługa serwisowa salonów kosmetycznych','serwis laserów dla sieci salonów']:assert phrase in main.text().lower(),phrase
 for peer in locales.published(g).values():assert any(n.attrs.get('href')==peer for n in p['tree'].all('a'))
 assert 'G-6QFRWP5RX5' in p['source'] and 'AW-17614450660' in p['source']
print('PASS: B2B PL/RU/EN, SEO, six FAQs, three steps, form fields, locale links and existing analytics IDs')
