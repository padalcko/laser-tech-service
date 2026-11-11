#!/usr/bin/env python3
"""Build only public files, preserving routes and exact HTML/resource bytes."""
import shutil
from html import escape
import xml.etree.ElementTree as ET
from public_site import ROOT, BASE, public_files, Page, route

DIST = ROOT / 'dist'

def main():
    files = public_files()  # Discover before creating dist; never copy the repo wholesale.
    if DIST.is_symlink():
        raise RuntimeError(f'Refusing to replace symlink: {DIST}')
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir()
    for rel in files:
        target = DIST / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, target)
    # Preserve the curated sitemap verbatim; append new canonical source pages.
    # The locale registry still owns curated translation groups, not packaging.
    sitemap = (DIST / 'sitemap.xml').read_text()
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    known = {n.text for n in ET.fromstring(sitemap).findall('s:url/s:loc', ns)}
    additions = []
    for rel in files:
        if rel.suffix not in ('.html', '.htm'): continue
        page = Page((ROOT / rel).read_text())
        url = BASE + route(rel)
        if not page.noindex and page.canonicals == [url] and url not in known:
            links = ''.join(f'<xhtml:link rel="alternate" hreflang="{escape(lang, quote=True)}" href="{escape(href, quote=True)}" />' for lang, href in page.alternates)
            additions.append(f'  <url><loc>{escape(url)}</loc>{links}</url>\n')
    if additions:
        sitemap = sitemap.replace('</urlset>', ''.join(additions) + '</urlset>')
        (DIST / 'sitemap.xml').write_text(sitemap)
    print(f'Packaged {len(files)} public files; added {len(additions)} discovered sitemap URLs')

if __name__ == '__main__': main()
