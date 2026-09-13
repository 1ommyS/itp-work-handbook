"""Validate nav coverage, unfinished pages and the built site's local links."""

from __future__ import annotations

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]


def config() -> dict:
    # BaseLoader reads !ENV tags without evaluating the MkDocs configuration.
    return yaml.load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"), Loader=yaml.BaseLoader)


def nav_paths(node: object):
    if isinstance(node, str):
        yield node
    elif isinstance(node, list):
        for item in node:
            yield from nav_paths(item)
    elif isinstance(node, dict):
        for item in node.values():
            yield from nav_paths(item)


def check_source() -> list[str]:
    docs = ROOT / "docs"
    actual = {p.relative_to(docs).as_posix() for p in docs.rglob("*.md")}
    paths = list(nav_paths(config()["nav"]))
    errors = []
    for path in sorted(set(paths) - actual):
        errors.append(f"Navigation points to a missing page: {path}")
    for path in sorted(actual - set(paths)):
        errors.append(f"Page is not in navigation: {path}")
    for path, count in Counter(paths).items():
        if count > 1:
            errors.append(f"Page occurs {count} times in navigation: {path}")
    for path in sorted(actual):
        source = (docs / path).read_text(encoding="utf-8")
        if len(source.strip()) < 160:
            errors.append(f"Empty or very short page: {path}")
        if len(re.findall(r"^# [^#].+$", source, flags=re.MULTILINE)) != 1:
            errors.append(f"Expected exactly one top-level title: {path}")
        if re.search(r"^\s*(?:TODO|TBD|WIP|ЗАГЛУШКА)(?:\b|:)", source, flags=re.MULTILINE):
            errors.append(f"Unfinished content marker: {path}")

    java_ranges = {
        "interview-bank/java-core.md": range(1, 81),
        "interview-bank/java-runtime.md": range(81, 161),
        "interview-bank/java-ecosystem.md": range(161, 241),
    }
    for path, expected in java_ranges.items():
        page = docs / path
        if not page.is_file():
            continue
        numbers = [int(value) for value in re.findall(
            r"^\*\*(\d+)\.", page.read_text(encoding="utf-8"), flags=re.MULTILINE
        )]
        if numbers != list(expected):
            errors.append(f"Java question numbering is incomplete in {path}")

    leetcode = docs / "interview-bank/leetcode-50.md"
    if leetcode.is_file():
        slugs = re.findall(
            r"https://leetcode\.com/problems/([^/]+)/", leetcode.read_text(encoding="utf-8")
        )
        if len(slugs) != 50 or len(set(slugs)) != 50:
            errors.append("LeetCode collection must contain 50 unique problem links")
    print(f"Checked {len(actual)} source pages and {len(paths)} navigation entries.")
    return errors


class Page(HTMLParser):
    def __init__(self, path: Path):
        super().__init__()
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if data.get("id"):
            self.ids.add(data["id"])
        if tag == "a" and data.get("href"):
            self.links.append(data["href"])
        if tag in {"img", "script"} and data.get("src"):
            self.links.append(data["src"])
        if tag == "link" and data.get("href") and data.get("rel") != "canonical":
            self.links.append(data["href"])


def check_site() -> list[str]:
    site = (ROOT / "site").resolve()
    pages = {p.resolve(): Page(p) for p in site.rglob("*.html")}
    errors: set[str] = set()
    prefix = urlsplit(config()["site_url"]).path.rstrip("/")
    count = 0
    for path, page in pages.items():
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            count += 1
            local = unquote(url.path)
            if local.startswith("/"):
                if prefix and (local == prefix or local.startswith(prefix + "/")):
                    local = local[len(prefix):]
                target = site / local.lstrip("/")
            else:
                target = path.parent / local if local else path
            target = target.resolve()
            if target.is_dir():
                target /= "index.html"
            label = f"{path.relative_to(site)} -> {link}"
            if not target.is_relative_to(site) or not target.is_file():
                errors.add(f"Missing local target: {label}")
            elif url.fragment and target in pages:
                fragment = unquote(url.fragment)
                if fragment not in pages[target].ids:
                    errors.add(f"Missing anchor #{fragment}: {label}")
    print(f"Checked {len(pages)} HTML pages and {count} local link/asset references.")
    return sorted(errors)


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in {"source", "site"}:
        raise SystemExit("Usage: python scripts/check_docs.py source|site")
    errors = check_source() if sys.argv[1] == "source" else check_site()
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        raise SystemExit(1)
    print("All checks passed.")
