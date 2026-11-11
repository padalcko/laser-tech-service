#!/usr/bin/env python3
"""Fail closed on lost pages/assets, stale output, broken local links and SEO routes."""
import collections
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from public_site import ROOT, BASE, Page, public_files, route, local_path


def audit(root=ROOT):
    dist = root / 'dist'
    files = public_files(root)
    expected = set(files)
    actual = {p.relative_to(dist) for p in dist.rglob('*') if p.is_file()}
    errors = []; warnings = []; pages = []
    def error(kind, source, target=''):
        errors.append({'kind': kind, 'source': str(source), 'target': str(target)})
    redirects = []
    redirect_file = dist / '_redirects'
    if redirect_file.exists():
        for line in redirect_file.read_text().splitlines():
            parts = line.split('#', 1)[0].split()
            if len(parts) >= 2:
                pattern = re.escape(parts[0]).replace(r'\*', '(?P<splat>.*)')
                pattern = re.sub(r':([A-Za-z_]+)', r'(?P<\1>[^/]+)', pattern)
                redirects.append((re.compile('^' + pattern + '$'), parts[1], parts[2] if len(parts)>2 else '301'))
    def resolve(url, seen=()):
        path = local_path(url)
        if path is None: return True
        if path in seen or len(seen) > 16: return False
        rel = Path(path.lstrip('/'))
        candidates = [rel, rel / 'index.html']
        if not rel.suffix: candidates.append(Path(str(rel) + '.html'))
        exists = any(p in actual for p in candidates)
        for pattern, target, status in redirects:
            match = pattern.fullmatch(path)
            if match and ('!' in status or not exists):
                for name, value in match.groupdict().items(): target = target.replace(':' + name, value)
                return resolve(target, (*seen, path))
        return exists
    for rel in sorted(expected - actual): error('missing-file', rel)
    for rel in sorted(actual - expected): error('unexpected-public-file', rel)
    for rel in sorted(expected & actual):
        if rel.as_posix() != 'sitemap.xml' and (root / rel).read_bytes() != (dist / rel).read_bytes():
            error('stale-or-modified-file', rel)
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9', 'x': 'http://www.w3.org/1999/xhtml'}
    sitemap_urls = []
    try:
        tree = ET.parse(dist / 'sitemap.xml')
        sitemap_urls = [n.text for n in tree.findall('s:url/s:loc', ns)]
        for url in sitemap_urls:
            if not url or not url.startswith(BASE + '/') or not resolve(url): error('invalid-sitemap-url', 'sitemap.xml', url)
        for node in tree.findall('s:url/x:link', ns):
            if not resolve(node.get('href', '')): error('broken-sitemap-alternate', 'sitemap.xml', node.get('href'))
        if len(sitemap_urls) != len(set(sitemap_urls)): error('duplicate-sitemap-url', 'sitemap.xml')
    except (OSError, ET.ParseError) as exc: error('invalid-sitemap', 'sitemap.xml', exc)
    htmls = [p for p in files if p.suffix in ('.html', '.htm')]
    indexed = set(); parsed = {}
    for rel in htmls:
        before = len(errors)
        page = Page((root / rel).read_text())
        url = route(rel)
        lang = 'ru' if url.startswith('/ru/') else 'en' if url.startswith('/en/') else 'pl'
        parsed[url] = page
        if page.lang != lang: error('wrong-language', rel, page.lang)
        if not page.title: error('missing-title', rel)
        if not page.noindex:
            if page.canonicals != [BASE + url]: error('wrong-canonical', rel, page.canonicals)
            if not page.description: error('missing-description', rel)
            indexed.add(BASE + url)
            if BASE + url not in sitemap_urls: error('missing-sitemap-page', rel)
        elif BASE + url in sitemap_urls: error('noindex-in-sitemap', rel)
        for taglang, href in page.alternates:
            target = local_path(href, url)
            if target is None or not resolve(href): error('invalid-hreflang', rel, href)
            elif taglang != 'x-default':
                targetlang = 'ru' if target.startswith('/ru/') else 'en' if target.startswith('/en/') else 'pl'
                if taglang.split('-')[0] != targetlang: error('wrong-hreflang-language', rel, href)
        for kind, value in page.refs:
            target = local_path(value, page.base or url)
            if target is not None and not resolve(target): error('broken-' + kind, rel, value)
        pages.append({'source': rel.as_posix(), 'dist': rel in actual, 'url': url, 'language': page.lang,
                      'seo_preserved': rel in actual and (root / rel).read_bytes() == (dist / rel).read_bytes(),
                      'noindex': page.noindex, 'assets_and_links': len(errors)==before,
                      'status': 'ready' if len(errors)==before and rel in actual else 'error'})
    for url in sitemap_urls:
        if url not in indexed: error('sitemap-not-canonical-page', 'sitemap.xml', url)
    for url, page in parsed.items():
        for lang, href in page.alternates:
            target = parsed.get(local_path(href, url))
            if target and lang != 'x-default' and not any(l.split('-')[0] == page.lang and h == BASE + url for l, h in target.alternates):
                error('nonreciprocal-hreflang', url, href)
    # CSS references include fonts, backgrounds, imports; JS literal local resources
    # are checked too (computed URLs require browser/runtime testing).
    css_url = re.compile(r'url\(\s*[\'"]?([^\s)\'";]+)')
    css_import = re.compile(r'@import\s+[\'"]([^\'"]+)')
    js_url = re.compile(r'''["'](/(?:img|css|js|files)/[^"'\s${}]+|/ai-catalog\.json)["']''')
    for rel in files:
        if rel.suffix not in ('.css', '.js', '.mjs'): continue
        source = (dist / rel) if rel in actual else (root / rel)
        text = source.read_text()
        refs = css_url.findall(text) + css_import.findall(text) if rel.suffix == '.css' else js_url.findall(text)
        for value in refs:
            target = local_path(value, '/' + rel.as_posix())
            if target is not None and not resolve(target): error('broken-resource-reference', rel, value)
    for pattern, target, status in redirects:
        if ':' not in target and not resolve(target): error('broken-redirect-target', '_redirects', target)
    for service in ('robots.txt', '_headers', '_redirects', '404.html'):
        if Path(service) not in actual: error('missing-service-file', service)
    # Keep per-page readiness consistent with byte comparison errors recorded earlier.
    for page in pages:
        if any(e['source'] in (page['source'], page['url']) for e in errors): page['status'] = 'error'
    return {'status': 'FAIL' if errors else 'PASS', 'source_pages': len(htmls),
            'dist_pages': sum(p.suffix in ('.html', '.htm') for p in actual),
            'languages': dict(collections.Counter(p['language'] for p in pages)),
            'public_files': len(files), 'sitemap_urls': len(sitemap_urls),
            'missing_pages': [p.as_posix() for p in htmls if p not in actual],
            'dist_only_pages': sorted(p.as_posix() for p in actual - expected if p.suffix in ('.html', '.htm')),
            'pages': pages, 'errors': errors, 'warnings': warnings}

if __name__ == '__main__':
    report = audit()
    target = ROOT / 'reports/dist-validation.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('pages', 'errors')}, ensure_ascii=False, indent=2))
    for error in report['errors'][:30]: print(json.dumps(error, ensure_ascii=False))
    print(f"{len(report['errors'])} critical errors; full inventory: {target.relative_to(ROOT)}")
    sys.exit(bool(report['errors']))
