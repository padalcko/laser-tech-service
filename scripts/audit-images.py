#!/usr/bin/env python3
# Development/audit utility; not used by the website at runtime.
"""Inventory raster assets and check local image URLs; requires Pillow."""
import hashlib, json, re, sys
from pathlib import Path
from urllib.parse import unquote, urlsplit
from html import unescape
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
EXT = {'.jpg','.jpeg','.png','.webp','.avif','.gif','.bmp','.tif','.tiff','.ico'}
PAT = re.compile(r'''(?:https?://[^\s"'<>(),;]+|(?:\.{0,2}/)?[\w%+@./-]+)\.(?:jpe?g|png|webp|avif|gif|bmp|tiff?|ico|svg)(?:\?[^\s"'<>)]*)?''', re.I)
def files():
    return [p for p in ROOT.rglob('*') if p.is_file() and not any(x.startswith('.') for x in p.relative_to(ROOT).parts)]
def resolve(url, source):
    u=urlsplit(unescape(url))
    if u.scheme and u.netloc not in ('lasertechservice.pl','www.lasertechservice.pl'): return None
    path=unquote(u.path)
    return (ROOT/path.lstrip('/') if path.startswith('/') or (source.suffix in ('.md', '.py') and path.startswith('img/')) else source.parent/path).resolve()
def audit():
    allfiles=files(); refs={}; missing=[]; redirects=[]
    for p in allfiles:
        if p.suffix.lower() in EXT or p.suffix.lower() in {'.pdf','.mp4','.woff','.woff2'} or p.name.startswith('image-audit') or p.name in {'audit-images.py', 'check-pharaon.py'}: continue
        try: text=p.read_text()
        except (UnicodeError,OSError): continue
        text = re.sub(r'data:[^\s\"\']+', '', text)
        for n,line in enumerate(text.splitlines(),1):
            for m in PAT.finditer(unescape(line)):
                url=m.group(); target=resolve(url,p)
                if target is None: continue
                # Redirect source URLs intentionally refer to removed legacy files.
                if p.name=='_redirects' and url==line.split()[0]: continue
                record={'file':str(p.relative_to(ROOT)),'line':n,'url':url}
                refs.setdefault(str(target),[]).append(record)
                if not target.is_file(): missing.append(record)
    rows=[]
    for p in allfiles:
        if p.suffix.lower() not in EXT: continue
        with Image.open(p) as im:
            rows.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'width':im.width,'height':im.height,'format':im.format,'alpha':im.mode in ('RGBA','LA') or 'transparency' in im.info,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'pixels_sha256':hashlib.sha256(im.convert('RGBA').tobytes()).hexdigest(),'references':refs.get(str(p),[]),'same_stem_alternatives':[str(q.relative_to(ROOT)) for q in p.parent.glob(p.stem+'.*') if q!=p and q.suffix.lower() in EXT]})
    return {'count':len(rows),'bytes':sum(r['bytes'] for r in rows),'images':rows,'missing':missing}
if __name__=='__main__':
    result=audit()
    if '--json' in sys.argv: print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        print(json.dumps({k:v for k,v in result.items() if k!='images'},indent=2))
        sys.exit(bool(result['missing']))
