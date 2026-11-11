"""Publication boundary shared by packaging and verification (stdlib only).

All non-private directories may contain pages; resource types, not page routes,
are allowlisted. New HTML directories need no registry/package-list edits.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, unquote
import os

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://lasertechservice.pl'
PRIVATE = {'dist', 'content', 'docs', 'reports', 'scripts', 'node_modules', '__pycache__', 'tests', 'coverage'}
EXTENSIONS = set('.html .htm .css .js .mjs .png .jpg .jpeg .webp .avif .gif .svg .ico .woff .woff2 .ttf .otf .eot .mp4 .webm .ogg .mp3 .wav .pdf .vtt'.split())
ROOT_DATA = {'robots.txt', 'sitemap.xml', 'llms.txt', 'llms-full.txt', 'ai-catalog.json', 'site.webmanifest', '_headers', '_redirects'}

def public_files(root=ROOT):
    result = []
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if not d.startswith('.') and d not in PRIVATE)
        for name in sorted(dirs + files):
            p = Path(directory) / name
            if p.is_symlink():
                raise ValueError(f'Symlinks are not publishable: {p.relative_to(root)}')
        for name in sorted(files):
            p = Path(directory) / name
            if name.startswith('.'):
                continue
            rel = p.relative_to(root)
            if p.suffix.lower() in EXTENSIONS or (len(rel.parts) == 1 and name in ROOT_DATA) or (name == 'index.md' and p.with_suffix('.html').is_file()):
                result.append(rel)
    return sorted(result)

def route(path):
    value = '/' + path.as_posix()
    return value[:-10] if value.endswith('index.html') else value

def local_path(value, base='/'):
    parsed = urlsplit(urljoin(BASE + base, value))
    if parsed.scheme not in ('http', 'https') or parsed.hostname not in ('lasertechservice.pl', 'www.lasertechservice.pl'):
        return None
    return unquote(parsed.path)

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.lang = ''; self.canonicals = []; self.alternates = []
        self.refs = []; self.noindex = False; self.base = None
        self.title = False; self.description = False
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html': self.lang = a.get('lang', '')
        if tag == 'title': self.title = True
        if tag == 'base': self.base = a.get('href')
        if tag == 'meta':
            if a.get('name', '').lower() in ('robots', 'googlebot') and 'noindex' in a.get('content', '').lower(): self.noindex = True
            if a.get('name') == 'description': self.description = bool(a.get('content'))
            if a.get('property') in ('og:image', 'og:video') or a.get('name') == 'twitter:image':
                self.refs.append(('asset', a.get('content', '')))
        if tag == 'link':
            rel = a.get('rel', '').split()
            if 'canonical' in rel: self.canonicals.append(a.get('href', ''))
            if a.get('hreflang'): self.alternates.append((a['hreflang'], a.get('href', '')))
        for key in ('src', 'href', 'poster', 'data-src'):
            if a.get(key) and tag != 'base': self.refs.append(('link' if tag in ('a', 'area') else 'asset', a[key]))
        for key in ('srcset', 'imagesrcset', 'data-srcset'):
            if a.get(key) and not a[key].startswith('data:'):
                self.refs.extend(('asset', part.strip().split()[0]) for part in a[key].split(',') if part.strip())
