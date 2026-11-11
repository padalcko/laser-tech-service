#!/usr/bin/env python3
"""End-to-end regression in an isolated checkout-shaped copy; no deploy/network."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]

def run(root, script, success=True):
    result = subprocess.run([sys.executable, str(root/'scripts'/script)], cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if (result.returncode == 0) != success:
        raise AssertionError(result.stdout[-12000:])
    return result

def hashes(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}

def main():
    with tempfile.TemporaryDirectory(prefix='lts-publication-') as temp:
        work = Path(temp)/'source'
        shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns('.git', 'dist', 'node_modules', '__pycache__', '.DS_Store', 'reports', 'docs'))
        routes = ['realizacje', 'blog', 'uslugi', 'ru/realizacje', 'ru/blog', 'ru/uslugi', 'en/case-studies', 'en/blog', 'en/services']
        fixtures = []
        for parent in routes:
            folder = work/parent/'publication-regression-fixture'
            assert not folder.exists()
            folder.mkdir(parents=True)
            fixtures.append(folder)
            lang = 'ru' if parent.startswith('ru/') else 'en' if parent.startswith('en/') else 'pl'
            url = '/' + str(folder.relative_to(work)) + '/'
            (folder/'photo.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"><rect width="10" height="10"/></svg>')
            (folder/'index.html').write_text(f'<!doctype html><html lang="{lang}"><head><title>Publication regression {parent}</title><meta name="description" content="Build fixture"><link rel="canonical" href="https://lasertechservice.pl{url}"><link rel="stylesheet" href="/css/main.css"></head><body><main><h1>Fixture</h1><img src="photo.svg" alt="Fixture"><a href="/">Home</a></main></body></html>')
        private = work/'new-private-fixture'; private.mkdir()
        (private/'secret.env').write_text('TEST_ONLY=true')
        (private/'notes.md').write_text('Private documentation')
        (private/'.env').write_text('TEST_ONLY=true')
        # noindex pages must publish but must not enter the sitemap.
        noindex = work/'publication-noindex-fixture.html'
        noindex.write_text('<html lang="pl"><head><title>Fixture</title><meta name="robots" content="noindex"></head><body>Fixture</body></html>')
        run(work, 'build-site.py')
        report = json.loads((work/'reports/dist-validation.json').read_text())
        assert report['status'] == 'PASS'
        assert not (work/'dist/new-private-fixture').exists()
        for folder in fixtures:
            target = work/'dist'/folder.relative_to(work)
            assert (target/'index.html').is_file() and (target/'photo.svg').is_file()
            assert '/' + str(folder.relative_to(work)) + '/' in (work/'dist/sitemap.xml').read_text()
        # Detect missing HTML, missing image, stale HTML and an accidental secret together.
        first = work/'dist'/fixtures[0].relative_to(work)
        (first/'index.html').unlink()
        (first/'photo.svg').unlink()
        second = work/'dist'/fixtures[1].relative_to(work)/'index.html'
        second.write_text(second.read_text()+'<!-- corruption -->')
        (work/'dist/.env').write_text('TEST_ONLY=true')
        run(work, 'validate-dist.py', success=False)
        failed = json.loads((work/'reports/dist-validation.json').read_text())
        kinds = {e['kind'] for e in failed['errors']}
        assert {'missing-file', 'stale-or-modified-file', 'unexpected-public-file', 'broken-asset'} <= kinds, kinds
        # A source broken link cannot be hidden by byte-perfect copying.
        source = fixtures[2]/'index.html'; source.write_text(source.read_text().replace('href="/"', 'href="/missing-regression-target/"'))
        run(work, 'package-site.py')
        run(work, 'validate-dist.py', success=False)
        assert any(e['kind']=='broken-link' for e in json.loads((work/'reports/dist-validation.json').read_text())['errors'])
        for folder in fixtures: shutil.rmtree(folder)
        noindex.unlink(); shutil.rmtree(private)
        run(work, 'build-site.py')
        clean = json.loads((work/'reports/dist-validation.json').read_text())
        assert clean['status']=='PASS' and clean['source_pages']==report['source_pages']-10
        assert not any('fixture' in str(p) for p in (work/'dist').rglob('*'))
        before = hashes(work/'dist')
        run(work, 'build-site.py')
        assert before == hashes(work/'dist'), 'Build is not reproducible'
        evidence = {'status':'PASS', 'new_routes':routes, 'fixture_pages':10,
                    'private_files_excluded':True, 'negative_checks':sorted(kinds | {'broken-link'}),
                    'cleanup_build':'PASS', 'repeat_build_identical':True, 'final_pages':clean['source_pages']}
        (ROOT/'reports').mkdir(exist_ok=True)
        (ROOT/'reports/dist-regression.json').write_text(json.dumps(evidence,indent=2)+'\n')
        print(json.dumps(evidence,indent=2))

if __name__ == '__main__': main()
