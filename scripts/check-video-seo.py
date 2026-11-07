#!/usr/bin/env python3
"""Validate VideoObject coverage and publication metadata against the source manifest."""
import importlib.util
import json
from pathlib import Path
import sys
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("video_metadata", ROOT / "scripts" / "build-video-metadata.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
manifest = json.loads(builder.MANIFEST.read_text(encoding="utf-8"))
videos = manifest["videos"]
issues = []
seen = {}
counts = {"html_pages": 0, "video_pages": 0, "video_objects": 0}

for path in ROOT.rglob("*.html"):
    if ".git" in path.relative_to(ROOT).parts or "dist" in path.relative_to(ROOT).parts:
        continue
    counts["html_pages"] += 1
    source = path.read_text(encoding="utf-8")
    builder.localized_language(source)
    iframe_parser = builder.VideoIframeParser()
    iframe_parser.feed(source)
    iframe_ids = [video_id for video_id, _ in iframe_parser.videos]
    if len(iframe_ids) != len(set(iframe_ids)):
        issues.append(f"{path.relative_to(ROOT)}: duplicate visible YouTube iframe")

    objects = {}
    for match in builder.JSON_LD.finditer(source):
        try:
            data = json.loads(match.group(2))
        except ValueError as error:
            issues.append(f"{path.relative_to(ROOT)}: invalid JSON-LD: {error}")
            continue
        for item in builder.walk(data):
            video_id = builder.youtube_id(item.get("embedUrl", "")) or builder.youtube_id(item.get("contentUrl", ""))
            if not video_id:
                continue
            if video_id in objects:
                issues.append(f"{path.relative_to(ROOT)}: duplicate VideoObject for {video_id}")
                continue
            objects[video_id] = item

    if iframe_ids:
        counts["video_pages"] += 1
    if set(iframe_ids) != set(objects):
        issues.append(
            f"{path.relative_to(ROOT)}: visible/schema video IDs differ "
            f"(iframes={sorted(set(iframe_ids))}, schemas={sorted(objects)})"
        )

    for video_id, item in objects.items():
        counts["video_objects"] += 1
        video = videos.get(video_id)
        if not video:
            issues.append(f"{path.relative_to(ROOT)}: {video_id} missing from source manifest")
            continue
        for field in ("name", "description", "thumbnailUrl", "uploadDate", "duration", "embedUrl"):
            if not item.get(field):
                issues.append(f"{path.relative_to(ROOT)}: {video_id} missing {field}")
        expected_date = builder.publication_date(video)
        if item.get("uploadDate") != expected_date:
            issues.append(f"{path.relative_to(ROOT)}: {video_id} uploadDate is not the Warsaw conversion")
        else:
            actual = datetime.fromisoformat(item["uploadDate"])
            if actual.tzinfo is None or actual.utcoffset() != actual.astimezone(builder.WARSAW).utcoffset():
                issues.append(f"{path.relative_to(ROOT)}: {video_id} uploadDate has the wrong Warsaw offset")
        if item.get("duration") != video["duration"]:
            issues.append(f"{path.relative_to(ROOT)}: {video_id} duration differs from YouTube metadata")
        if item.get("thumbnailUrl") != f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg":
            issues.append(f"{path.relative_to(ROOT)}: {video_id} thumbnail is not the verified YouTube thumbnail")
        if item.get("embedUrl") != f"https://www.youtube.com/embed/{video_id}":
            issues.append(f"{path.relative_to(ROOT)}: {video_id} has a noncanonical embedUrl")
        content_url = item.get("contentUrl", "")
        if content_url and (builder.urlsplit(content_url).hostname or "").lower().endswith("youtube.com"):
            issues.append(f"{path.relative_to(ROOT)}: {video_id} uses a YouTube watch page as contentUrl")
        seen.setdefault(video_id, set()).add(item["uploadDate"])

if set(seen) != set(videos):
    issues.append(f"Manifest/video coverage differs (manifest={sorted(videos)}, page schemas={sorted(seen)})")
for video_id, dates in seen.items():
    if len(dates) != 1:
        issues.append(f"{video_id} has inconsistent uploadDate values across language pages")

jan = datetime.fromisoformat("2026-01-15T12:00:00+00:00").astimezone(builder.WARSAW)
jul = datetime.fromisoformat("2026-07-15T12:00:00+00:00").astimezone(builder.WARSAW)
if jan.strftime("%z") != "+0100" or jul.strftime("%z") != "+0200":
    issues.append("Europe/Warsaw winter/summer UTC offsets are incorrect")
dst_cases = [
    ("2026-03-29T00:30:00+00:00", "+0100"),
    ("2026-03-29T01:30:00+00:00", "+0200"),
    ("2026-10-25T00:30:00+00:00", "+0200"),
    ("2026-10-25T01:30:00+00:00", "+0100"),
]
for value, expected_offset in dst_cases:
    if datetime.fromisoformat(value).astimezone(builder.WARSAW).strftime("%z") != expected_offset:
        issues.append(f"Europe/Warsaw DST transition failed for {value}")

if issues:
    print("\n".join(issues), file=sys.stderr)
    raise SystemExit(1)
print(json.dumps({
    **counts,
    "unique_videos": len(seen),
    "winter_offset": jan.strftime("%z"),
    "summer_offset": jul.strftime("%z"),
    "dst_transitions": "PASS",
    "issues": [],
}, ensure_ascii=False, indent=2))
