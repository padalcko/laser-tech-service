#!/usr/bin/env python3
"""Prepare critical resource links, prune unused Jarallax scripts, and build responsive WebP candidates.

Run after site generators. Full image generation requires Pillow from
scripts/requirements-performance.txt; the normal site build uses --html-only.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import argparse
import io
import re

ROOT = Path(__file__).resolve().parents[1]
FONT_STYLESHEET = (
    'https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,500;0,600;0,700;0,800;1,700&amp;display=swap'
)
RESOURCE_LINKS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com" />',
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />',
    f'<link rel="stylesheet" href="{FONT_STYLESHEET}" />',
    '<link rel="stylesheet" href="/css/reset.css" />',
)
MAIN_STYLESHEET = re.compile(r'<link\b(?=[^>]*\bhref=["\']/css/main\.css["\'])[^>]*>', re.I)
SCRIPT_TAG = re.compile(
    r'(?im)^[ \t]*<script\b[^>]*\bsrc=["\'][^"\']*jarallax[^"\']*["\'][^>]*>\s*</script>[ \t]*(?:\r?\n)?'
)
VOID_TAGS = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

SIZES = {
    'case-gallery': '(max-width: 650px) calc(100vw - 48px), (max-width: 900px) calc((100vw - 64px) / 2), (max-width: 1248px) calc((100vw - 80px) / 3), 374px',
    'case-gallery--compact': '(max-width: 649px) calc((100vw - 60px) / 2), (max-width: 1248px) calc((100vw - 84px) / 4), 279px',
    'case-gallery--four': '(max-width: 650px) calc(100vw - 48px), (max-width: 900px) calc((100vw - 64px) / 2), (max-width: 1200px) calc((100vw - 96px) / 4), 276px',
    'case-hero__image': '(max-width: 900px) calc(100vw - 48px), 500px',
    'case-work-image': '(max-width: 650px) calc(100vw - 51px), (max-width: 900px) calc(100vw - 63px), (max-width: 1214px) calc((100vw - 138px) * 0.475), 512px',
    'case-work-image-compact': '(max-width: 369px) calc(100vw - 51px), 318px',
    'article-image': '(max-width: 1000px) calc(100vw - 40px), 960px',
    'device': '(max-width: 650px) 170px, 220px',
    'ba-images': '(max-width: 650px) calc((100vw - 48px) / 2), (max-width: 900px) calc((100vw - 73px) / 4), (max-width: 1200px) calc((100vw - 98px) / 6), 184px',
    'realizacja-card__image': '(max-width: 650px) calc(100vw - 38px), (max-width: 848px) calc(100vw - 50px), (max-width: 900px) 798px, (max-width: 1200px) calc((100vw - 110px) / 3), 363px',
    'error-image': '(max-width: 620px) calc(100vw - 68px), (max-width: 650px) calc(100vw - 78px), (max-width: 760px) calc(100vw - 90px), (max-width: 1050px) min(848px, calc(100vw - 90px)), (max-width: 1239px) calc(56vw - 85px), 610px',
    'service-case': '(min-width: 1200px) 280px, (min-width: 1024px) 22vw, (min-width: 650px) 45vw, 90vw',
    'service-case-landing': '(min-width: 1200px) 233px, (min-width: 1024px) calc((100vw - 268px) / 4), (min-width: 650px) calc((100vw - 148px) / 2), calc(100vw - 88px)',
}
WIDTHS = {
    'case-gallery': (320, 480, 640, 960),
    'case-gallery--compact': (200, 320, 480, 640),
    'case-gallery--four': (320, 480, 640, 960),
    'case-hero__image': (320, 480, 640, 960),
    'case-work-image': (320, 480, 640, 960),
    'case-work-image-compact': (200, 320, 480, 640),
    'article-image': (320, 480, 640, 960),
    'device': (200, 320, 480),
    'ba-images': (200, 320, 480),
    'realizacja-card__image': (200, 320, 480, 640),
    'error-image': (320, 480, 640, 960),
    'service-case': (200, 320, 640, 960),
    'service-case-landing': (200, 320, 640, 960),
}
CLASS_ORDER = (
    'case-gallery--compact', 'case-gallery--four', 'case-gallery',
    'case-hero__image', 'case-work-image', 'article-image', 'device', 'ba-images',
    'realizacja-card__image', 'error-image',
    'service-case-landing', 'service-case',
)


class ImageParser(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.stack = []
        self.images = []
        self.line_offsets = [0]
        self.line_offsets.extend(index + 1 for index, char in enumerate(source) if char == '\n')

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'img':
            classes = set(attrs.get('class', '').split())
            ancestor_classes = [parent_classes for _, parent_classes, _ in self.stack]
            for parent_classes in ancestor_classes:
                classes.update(parent_classes)
            category = next((name for name in CLASS_ORDER if name in classes), None)
            if category:
                if category == 'case-work-image' and 'case-photo--compact' in classes:
                    category = 'case-work-image-compact'
                if category == 'service-case' and any('service-landing' in parent for parent in ancestor_classes):
                    category = 'service-case-landing'
                styles = [attrs.get('style', '')]
                styles.extend(style for _, _, style in reversed(self.stack))
                max_width = None
                for style in styles:
                    match = re.search(r'\bmax-width\s*:\s*(\d+)\s*px\b', style, re.I)
                    if match:
                        max_width = int(match.group(1))
                        break
                line, column = self.getpos()
                start = self.line_offsets[line - 1] + column
                raw = self.get_starttag_text()
                self.images.append({
                    'start': start,
                    'end': start + len(raw),
                    'tag': raw,
                    'attrs': attrs,
                    'category': category,
                    'max_width': max_width,
                })
        if tag not in VOID_TAGS:
            self.stack.append((tag, set(attrs.get('class', '').split()), attrs.get('style', '')))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break


def insert_attributes(tag, attrs):
    end = re.search(r'\s*/?>$', tag)
    if not end:
        raise ValueError(f'Could not locate end of image tag: {tag[:100]}')
    return f'{tag[:end.start()].rstrip()} {attrs}{tag[end.start():]}'


def with_resource_links(source):
    match = MAIN_STYLESHEET.search(source)
    if not match:
        return source
    head = source[:match.start()]
    missing = []
    checks = (
        ('href="https://fonts.googleapis.com"', RESOURCE_LINKS[0]),
        ('href="https://fonts.gstatic.com"', RESOURCE_LINKS[1]),
        ('fonts.googleapis.com/css2?family=Montserrat', RESOURCE_LINKS[2]),
        ('href="/css/reset.css"', RESOURCE_LINKS[3]),
    )
    for token, link in checks:
        if token not in head:
            missing.append(link)
    return source[:match.start()] + '\n    '.join(missing) + ('\n    ' if missing else '') + source[match.start():]


def image_path_for(url, page):
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc:
        return None
    path = (ROOT / parsed.path.lstrip('/')) if parsed.path.startswith('/') else (page.parent / parsed.path)
    return path.resolve()


def image_tools():
    try:
        from PIL import Image, ImageOps
    except ImportError as error:
        raise SystemExit(
            'Responsive WebP generation requires Pillow. Install it with '
            'python3 -m pip install -r scripts/requirements-performance.txt'
        ) from error
    return Image, ImageOps


def image_dimensions(path, Image):
    with Image.open(path) as image:
        return image.size


def ratio_matches(source_size, candidate_size):
    scaled_height = source_size[1] * candidate_size[0] / source_size[0]
    return candidate_size[1] in (int(scaled_height), int(scaled_height) + 1)


def candidate_variant(source, width, original_size, Image, allow_legacy):
    paths = [source.with_name(f'{source.stem}-responsive-{width}w.webp')]
    if allow_legacy:
        paths.append(source.with_name(f'{source.stem}-{width}w{source.suffix}'))
    for path in paths:
        if not path.is_file():
            continue
        dimensions = image_dimensions(path, Image)
        if dimensions[0] == width and ratio_matches(original_size, dimensions) and path.stat().st_size < source.stat().st_size:
            return path
    return None


def make_variant(source, width, original_size, Image, ImageOps, generate):
    target = source.with_name(f'{source.stem}-responsive-{width}w.webp')
    if target.is_file() and target.stat().st_mtime >= source.stat().st_mtime:
        dimensions = image_dimensions(target, Image)
        if dimensions[0] == width and ratio_matches(original_size, dimensions) and target.stat().st_size < source.stat().st_size:
            return target
    if not generate:
        return None
    with Image.open(source) as source_image:
        if getattr(source_image, 'n_frames', 1) != 1:
            return None
        image = ImageOps.exif_transpose(source_image)
        if image.width != original_size[0] or image.height != original_size[1]:
            return None
        height = max(1, round(image.height * width / image.width))
        converted = image.convert('RGBA' if 'A' in image.getbands() else 'RGB')
        output = io.BytesIO()
        options = {'format': 'WEBP', 'quality': 92, 'method': 6}
        icc_profile = source_image.info.get('icc_profile')
        exif = source_image.info.get('exif')
        if icc_profile:
            options['icc_profile'] = icc_profile
        if exif:
            options['exif'] = exif
        converted.resize((width, height), Image.Resampling.LANCZOS).save(output, **options)
    data = output.getvalue()
    if len(data) >= source.stat().st_size:
        return None
    target.write_bytes(data)
    return target


def responsive_candidates(src, page, category, Image, ImageOps, generate):
    source = image_path_for(src, page)
    if not source or not source.is_file() or source.suffix.lower() not in {'.webp', '.png', '.jpg', '.jpeg'}:
        return None
    original_size = image_dimensions(source, Image)
    if original_size[0] < 2 or original_size[1] < 2:
        return None
    candidates = {}
    for width in WIDTHS[category]:
        if width >= original_size[0]:
            continue
        variant = candidate_variant(
            source, width, original_size, Image, allow_legacy=category != 'service-case',
        )
        if variant is None:
            variant = make_variant(source, width, original_size, Image, ImageOps, generate)
        if variant:
            candidates[width] = '/' + variant.relative_to(ROOT).as_posix()
    candidates[original_size[0]] = src
    return ', '.join(f'{url} {width}w' for width, url in sorted(candidates.items()))


def image_sizes(image):
    if image['category'] == 'article-image' and image['max_width']:
        max_width = image['max_width']
        return f'(max-width: {max_width + 40}px) calc(100vw - 40px), {max_width}px'
    return SIZES[image['category']]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--html-only', action='store_true', help='Update stylesheet links and remove unused Jarallax scripts without generating image variants.')
    parser.add_argument('--check', action='store_true', help='Verify generated resources and responsive image markup without modifying files.')
    args = parser.parse_args()
    Image = ImageOps = None
    if not args.html_only:
        Image, ImageOps = image_tools()

    changed = {'html': 0, 'srcsets': 0, 'jarallax_scripts': 0}
    for page in sorted(ROOT.rglob('*.html')):
        if any(part in {'.git', 'dist', 'node_modules', 'docs', 'reports'} for part in page.relative_to(ROOT).parts):
            continue
        original = page.read_text()
        source = with_resource_links(original)
        has_parallax = bool(re.search(r'\bdata-jarallax(?:\s|=|>)|\bclass=["\'][^"\']*\bjarallax\b', source, re.I))
        removed_scripts = sum(
            1 for match in SCRIPT_TAG.finditer(source)
            if 'jarallax-video' in match.group(0).lower() or not has_parallax
        )
        source = SCRIPT_TAG.sub(
            lambda match: (
                '' if 'jarallax-video' in match.group(0).lower() or not has_parallax
                else match.group(0)
            ),
            source,
        )
        changed['jarallax_scripts'] += removed_scripts

        if not args.html_only:
            image_parser = ImageParser(source)
            image_parser.feed(source)
            replacements = []
            for image in image_parser.images:
                preserve_srcset = image['category'] in {
                    'case-work-image', 'case-work-image-compact', 'realizacja-card__image',
                } and image['attrs'].get('srcset')
                src = image['attrs'].get('src')
                if not src and not preserve_srcset:
                    continue
                srcset = image['attrs']['srcset'] if preserve_srcset else responsive_candidates(
                    src, page, image['category'], Image, ImageOps, generate=not args.check,
                )
                if not srcset:
                    continue
                sizes = image_sizes(image)
                if image['attrs'].get('srcset') != srcset or image['attrs'].get('sizes') != sizes:
                    tag = image['tag']
                    updated = re.sub(r'\s+srcset=(["\']).*?\1', '', tag, flags=re.I)
                    updated = re.sub(r'\s+sizes=(["\']).*?\1', '', updated, flags=re.I)
                    updated = insert_attributes(updated, f'srcset="{srcset}" sizes="{sizes}"')
                    replacements.append((image['start'], image['end'], updated))
                    changed['srcsets'] += 1
            for start, end, updated in reversed(replacements):
                source = source[:start] + updated + source[end:]

        if source != original:
            if args.check:
                raise SystemExit(f'Performance resources are stale: {page.relative_to(ROOT)}')
            page.write_text(source)
            changed['html'] += 1

    if args.check:
        print('Performance resources and responsive image markup are current.')
        return
    print(
        f"Updated {changed['html']} HTML files; refreshed {changed['srcsets']} responsive image sets; "
        f"removed {changed['jarallax_scripts']} unused Jarallax script tags."
    )


if __name__ == '__main__':
    main()
