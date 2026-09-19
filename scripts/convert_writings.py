"""Convert numbered text files in writings/ into Jekyll posts."""

from __future__ import annotations

import datetime as dt
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "writings"
POSTS = ROOT / "_posts" / "auto"
PUBLIC_IMAGES = ROOT / "assets" / "images" / "posts"
IMAGE_EXTENSIONS = {".avif", ".gif", ".jpeg", ".jpg", ".png", ".svg", ".webp"}


def publication_date(source: Path) -> str:
    """Use the date the source entered Git, with today's date as a local fallback."""
    try:
        result = subprocess.run(
            [
                "git",
                "log",
                "--follow",
                "--diff-filter=A",
                "--format=%as",
                "--",
                source.relative_to(ROOT).as_posix(),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        dates = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        if dates:
            return dates[-1]
    except (OSError, subprocess.CalledProcessError):
        pass
    return dt.date.today().isoformat()


def slugify(value: str, number: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-")
    return slug or f"writing-{number}"


def repair_mojibake(value: str) -> str:
    """Repair text that was UTF-8 decoded once as Latin-1, when detectable."""
    if not any(marker in value for marker in ("Ã", "Ä", "Å", "â")):
        return value
    try:
        repaired = value.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return value
    return repaired


def read_draft(source: Path) -> tuple[str, list[str], str | None, str]:
    text = source.read_text(encoding="utf-8-sig").replace("\r\n", "\n").strip()
    if not text:
        raise ValueError(f"{source.relative_to(ROOT)} is empty")

    lines = text.splitlines()
    title_index = next((i for i, line in enumerate(lines) if line.strip()), None)
    if title_index is None:
        raise ValueError(f"{source.relative_to(ROOT)} has no title")

    title = repair_mojibake(re.sub(r"^#\s+", "", lines[title_index].strip()))
    tags: list[str] = []
    description = None
    body_start = title_index + 1

    while body_start < len(lines):
        line = lines[body_start].strip()
        if not line:
            body_start += 1
            continue
        match = re.match(r"(?i)^tags?\s*:\s*(.+)$", line)
        if match:
            tags = [tag.strip() for tag in match.group(1).split(",") if tag.strip()]
            body_start += 1
            continue
        match = re.match(r"(?i)^description\s*:\s*(.+)$", line)
        if match:
            description = match.group(1).strip()
            body_start += 1
            continue
        break

    body = "\n".join(lines[body_start:]).strip()
    if not body:
        raise ValueError(f"{source.relative_to(ROOT)} has a title but no article text")
    return title, tags, description, body


def copy_images(number: str) -> tuple[list[Path], Path | None]:
    source_dir = INBOX / "images" / number
    target_dir = PUBLIC_IMAGES / number
    if target_dir.exists():
        shutil.rmtree(target_dir)

    images = []
    if source_dir.is_dir():
        images = sorted(
            path for path in source_dir.iterdir()
            if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
        )
        if images:
            target_dir.mkdir(parents=True, exist_ok=True)
            for image in images:
                shutil.copy2(image, target_dir / image.name)

    cover = next((image for image in images if image.stem.lower() == "cover"), None)
    return images, cover


def insert_images(body: str, number: str, images: list[Path]) -> str:
    names = {image.name.lower(): image for image in images}
    marker = re.compile(r"\[place\s+([^\]]+)\s+here\]", re.IGNORECASE)

    def replacement(match: re.Match[str]) -> str:
        requested = Path(match.group(1).strip()).name.lower()
        image = names.get(requested)
        if image is None:
            raise ValueError(f"image marker refers to missing file: {match.group(1).strip()}")
        alt = image.stem.replace("-", " ").replace("_", " ").strip().capitalize()
        url = f"/assets/images/posts/{number}/{image.name}"
        return f"![{alt}]({url})"

    return marker.sub(replacement, body)


def make_post(source: Path) -> Path:
    number = source.stem
    title, tags, description, body = read_draft(source)
    date = publication_date(source)
    images, cover = copy_images(number)
    body = insert_images(body, number, images)
    filename = f"{date}-{number}-{slugify(title, number)}.md"

    front_matter = [
        "---",
        "layout: post",
        f"title: {json.dumps(title, ensure_ascii=False)}",
        f"date: {date} 00:00:00 +0530",
        f"generated_from: {json.dumps(source.relative_to(ROOT).as_posix())}",
    ]
    if description:
        front_matter.append(f"description: {json.dumps(description, ensure_ascii=False)}")
    if tags:
        front_matter.append(f"tags: {json.dumps(tags, ensure_ascii=False)}")
    if cover:
        cover_url = f"/assets/images/posts/{number}/{cover.name}"
        front_matter.extend(
            [
                f"thumbnail: {json.dumps(cover_url)}",
                f"image: {json.dumps(cover_url)}",
                f"image_alt: {json.dumps(title + ' cover image', ensure_ascii=False)}",
            ]
        )
    front_matter.extend(["---", "", body, ""])

    POSTS.mkdir(parents=True, exist_ok=True)
    target = POSTS / filename
    target.write_text("\n".join(front_matter), encoding="utf-8")
    return target


def main() -> int:
    drafts = sorted(
        (path for path in INBOX.glob("*.txt") if path.stem.isdigit()),
        key=lambda path: int(path.stem),
    )
    if POSTS.exists():
        shutil.rmtree(POSTS)
    if PUBLIC_IMAGES.exists():
        shutil.rmtree(PUBLIC_IMAGES)

    errors = []
    for draft in drafts:
        try:
            output = make_post(draft)
            print(f"Converted {draft.relative_to(ROOT)} -> {output.relative_to(ROOT)}")
        except ValueError as error:
            errors.append(str(error))

    if errors:
        for error in errors:
            print(f"Error: {error}", file=sys.stderr)
        return 1
    print(f"Converted {len(drafts)} writing(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
