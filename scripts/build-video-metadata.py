#!/usr/bin/env python3
"""Normalize visible YouTube VideoObject metadata from the versioned source manifest."""
import argparse
from datetime import datetime
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import parse_qs, urlsplit
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "content" / "video-metadata.json"
WARSAW = ZoneInfo("Europe/Warsaw")
JSON_LD = re.compile(
    r'(<script\b(?=[^>]*\btype=["\']application/ld\+json["\'])[^>]*>)'
    r'(.*?)'
    r'(</script\s*>)',
    re.IGNORECASE | re.DOTALL,
)


class VideoIframeParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.videos = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "iframe":
            return
        attributes = dict(attrs)
        video_id = youtube_id(attributes.get("src", ""))
        if video_id:
            self.videos.append((video_id, attributes.get("title", "")))


def youtube_id(url):
    parts = urlsplit(url)
    host = (parts.hostname or "").lower()
    segments = [part for part in parts.path.split("/") if part]
    if host in {"youtube.com", "www.youtube.com", "m.youtube.com", "youtube-nocookie.com", "www.youtube-nocookie.com"}:
        if len(segments) >= 2 and segments[0] in {"embed", "shorts"}:
            return segments[1]
        if segments == ["watch"]:
            return parse_qs(parts.query).get("v", [None])[0]
    if host in {"youtu.be", "www.youtu.be"} and segments:
        return segments[0]
    return None


def walk(value):
    if isinstance(value, dict):
        if value.get("@type") == "VideoObject":
            yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def localized_language(text):
    match = re.search(r"<html\b[^>]*\blang=[\"']([^\"']+)", text, re.IGNORECASE)
    if not match:
        raise ValueError("HTML document has no language attribute")
    language = match.group(1).lower().split("-", 1)[0]
    if language not in {"pl", "ru", "en"}:
        raise ValueError(f"Unsupported page language: {language}")
    return language


def publication_date(video):
    published_at = datetime.fromisoformat(video["publishedAt"])
    if published_at.tzinfo is None:
        raise ValueError("Video source publication timestamp must include its source offset")
    return published_at.astimezone(WARSAW).isoformat(timespec="seconds")


def set_video_metadata(video_object, video_id, video):
    video_object["uploadDate"] = publication_date(video)
    video_object["duration"] = video["duration"]
    video_object["thumbnailUrl"] = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
    video_object["embedUrl"] = f"https://www.youtube.com/embed/{video_id}"
    content_url = video_object.get("contentUrl")
    if content_url and (urlsplit(content_url).hostname or "").lower().endswith("youtube.com"):
        del video_object["contentUrl"]


def schema_script(video_id, video, language, title):
    localized = video.get("localized", {}).get(language)
    if not localized:
        raise ValueError(f"No localized metadata for unmarked video {video_id} on {language} page")
    if title != localized["name"]:
        raise ValueError(f"Visible iframe title mismatch for {video_id} on {language} page")
    schema = {
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "name": localized["name"],
        "description": localized["description"],
        "thumbnailUrl": f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
        "uploadDate": publication_date(video),
        "duration": video["duration"],
        "embedUrl": f"https://www.youtube.com/embed/{video_id}",
        "publisher": {
            "@type": "Organization",
            "name": "Laser Tech Service",
            "url": "https://lasertechservice.pl/",
            "@id": "https://lasertechservice.pl/#organization",
        },
        "inLanguage": language,
    }
    return '<script type="application/ld+json">\n' + json.dumps(schema, ensure_ascii=False, indent=2) + "\n</script>\n"


def transform(path, source, videos):
    language = localized_language(source)
    iframe_parser = VideoIframeParser()
    iframe_parser.feed(source)
    visible = {}
    for video_id, title in iframe_parser.videos:
        if video_id not in videos:
            raise ValueError(f"Missing source metadata for visible video {video_id} in {path}")
        if video_id in visible:
            raise ValueError(f"Duplicate visible video iframe {video_id} in {path}")
        visible[video_id] = title

    found = {}
    changed = False

    def update_script(match):
        nonlocal changed
        body = match.group(2)
        data = json.loads(body)
        video_objects = list(walk(data))
        if not video_objects:
            return match.group(0)
        for item in video_objects:
            video_id = youtube_id(item.get("embedUrl", "")) or youtube_id(item.get("contentUrl", ""))
            if not video_id:
                continue
            if video_id not in visible:
                raise ValueError(f"VideoObject {video_id} has no visible iframe in {path}")
            if video_id in found:
                raise ValueError(f"Duplicate VideoObject for {video_id} in {path}")
            found[video_id] = True
            set_video_metadata(item, video_id, videos[video_id])
        normalized = json.dumps(data, ensure_ascii=False, indent=2)
        leading = body[:len(body) - len(body.lstrip())]
        trailing = body[len(body.rstrip()):]
        rewritten = leading + normalized + trailing
        if rewritten != body:
            changed = True
        return match.group(1) + rewritten + match.group(3)

    result = JSON_LD.sub(update_script, source)
    missing = [video_id for video_id in visible if video_id not in found]
    if missing:
        insertion = "".join(
            schema_script(video_id, videos[video_id], language, visible[video_id])
            for video_id in missing
        )
        head_end = result.lower().rfind("</head>")
        if head_end < 0:
            raise ValueError(f"HTML document has no closing head tag: {path}")
        result = result[:head_end] + insertion + result[head_end:]
        changed = True
    return result, changed, len(missing)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated metadata is stale")
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("timezone") != "Europe/Warsaw":
        raise ValueError("Video metadata manifest must use Europe/Warsaw")
    videos = manifest["videos"]
    for video_id, video in videos.items():
        publication_date(video)
        if not re.fullmatch(r"PT(?:\d+H)?(?:\d+M)?(?:\d+S)", video.get("duration", "")):
            raise ValueError(f"Invalid ISO 8601 duration for {video_id}")

    updated = added = stale = 0
    for path in ROOT.rglob("*.html"):
        if ".git" in path.relative_to(ROOT).parts or "dist" in path.relative_to(ROOT).parts:
            continue
        source = path.read_text(encoding="utf-8")
        generated, changed, new_count = transform(path, source, videos)
        if changed:
            stale += 1
            if not args.check:
                path.write_text(generated, encoding="utf-8")
                updated += 1
        added += new_count

    if args.check and stale:
        raise SystemExit(f"Video metadata is stale in {stale} HTML files")
    print(json.dumps({
        "video_ids_in_manifest": len(videos),
        "new_video_objects": added,
        "updated_html_files": updated,
        "stale_html_files": stale,
    }, indent=2))


if __name__ == "__main__":
    main()
