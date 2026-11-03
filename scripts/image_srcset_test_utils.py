from pathlib import Path
import re


def assert_srcset_candidates(srcset, known_images, root):
    for candidate in srcset.split(','):
        path, descriptor = candidate.strip().split()
        assert descriptor.endswith('w'), candidate
        width = int(descriptor[:-1])
        if path in known_images:
            assert known_images[path]['width'] == width, candidate
        else:
            match = re.search(r'-responsive-(\d+)w\.webp$', path)
            assert match and int(match.group(1)) == width, candidate
        assert (Path(root) / path.lstrip('/')).is_file(), path


def normalize_performance_links(document):
    document = re.sub(
        r'\s*<link rel="(?:preconnect|stylesheet)" href="(?:https://fonts\.googleapis\.com|https://fonts\.gstatic\.com|/css/reset\.css)[^"]*"[^>]*>',
        '',
        document,
    )
    return re.sub(
        r'(?<!\n)\n(?= {0,8}<link rel="stylesheet" href="/css/main\.css")',
        '\n\n',
        document,
    )


def normalize_responsive_image_attributes(document):
    def normalize_tag(match):
        return re.sub(r'\s+(?:srcset|sizes)="[^"]+"', '', match[0])
    return re.sub(r'<img\b[^>]*>', normalize_tag, document, flags=re.S)
