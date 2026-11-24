#!/usr/bin/env python3
"""Build only public files, preserving routes and exact HTML/resource bytes."""
import shutil
import re
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
    root = re.search(r'<(?P<prefix>[A-Za-z_][\w.-]*:)?urlset\b[^>]*>', sitemap)
    if not root:
        raise ValueError('sitemap.xml has no urlset root')
    prefix = root.group('prefix') or ''
    xhtml = re.search(r'xmlns:(?P<prefix>[A-Za-z_][\w.-]*)="http://www.w3.org/1999/xhtml"', root.group())
    link_prefix = xhtml.group('prefix') if xhtml else 'xhtml'
    link_namespace = '' if xhtml else ' xmlns:xhtml="http://www.w3.org/1999/xhtml"'
    additions = []
    for rel in files:
        if rel.suffix not in ('.html', '.htm'): continue
        page = Page((ROOT / rel).read_text())
        url = BASE + route(rel)
        if not page.noindex and page.canonicals == [url] and url not in known:
            links = ''.join(f'<{link_prefix}:link{link_namespace} rel="alternate" hreflang="{escape(lang, quote=True)}" href="{escape(href, quote=True)}" />' for lang, href in page.alternates)
            additions.append(f'  <{prefix}url><{prefix}loc>{escape(url)}</{prefix}loc>{links}</{prefix}url>\n')
    if additions:
        closing = f'</{prefix}urlset>'
        if sitemap.count(closing) != 1:
            raise ValueError('sitemap.xml has no unique urlset closing tag')
        sitemap = sitemap.replace(closing, ''.join(additions) + closing)
        (DIST / 'sitemap.xml').write_text(sitemap)
    print(f'Packaged {len(files)} public files; added {len(additions)} discovered sitemap URLs')

if __name__ == '__main__': main()
