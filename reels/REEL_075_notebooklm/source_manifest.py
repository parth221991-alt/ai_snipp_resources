#!/usr/bin/env python3
r"""
NotebookLM source manifest — see your library at a glance before you upload.

NotebookLM's free tier caps a notebook at 50 sources, and its answers degrade
when the set is diluted with near-duplicates (5 articles rewriting one press
release make the model over-confident about that release). This script takes a
folder of files and/or a list of URLs and prints a clean, numbered,
de-duplicated manifest with warnings.

Zero dependencies — Python 3.9+ standard library only.

    python source_manifest.py --dir ./research
    python source_manifest.py --urls urls.txt
    python source_manifest.py --dir ./research --urls urls.txt
    python source_manifest.py --dir ./research --check      # warnings only

urls.txt: one URL per line, blank lines and #comments ignored.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from urllib.parse import urlparse

FREE_TIER_CAP = 50

# Extensions NotebookLM accepts as sources (as of 2026). Others are flagged.
SUPPORTED_EXT = {
    ".pdf", ".txt", ".md", ".markdown", ".docx", ".doc",
    ".rtf", ".csv", ".html", ".htm",
}

# Hosts that are usually low-signal as a *primary* source.
LOW_VALUE_HOSTS = {
    "medium.com", "substack.com", "linkedin.com", "reddit.com",
    "quora.com", "pinterest.com", "facebook.com", "x.com", "twitter.com",
}


def _kind(ext: str) -> str:
    return {
        ".pdf": "pdf", ".txt": "txt", ".md": "md", ".markdown": "md",
        ".docx": "doc", ".doc": "doc", ".rtf": "doc",
        ".csv": "csv", ".html": "web", ".htm": "web",
    }.get(ext, "?")


def scan_dir(root: Path) -> list[dict]:
    items: list[dict] = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.name.startswith("."):
            continue
        ext = p.suffix.lower()
        try:
            digest = hashlib.md5(p.read_bytes()[:65536]).hexdigest()[:10]
        except OSError:
            digest = "unreadable"
        items.append({
            "type": "file",
            "kind": _kind(ext) if ext in SUPPORTED_EXT else "unsupported",
            "label": p.name,
            "key": digest,
            "ext_ok": ext in SUPPORTED_EXT,
            "size_kb": p.stat().st_size // 1024,
        })
    return items


def scan_urls(path: Path) -> list[dict]:
    items: list[dict] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        host = (urlparse(line).hostname or "").lower().removeprefix("www.")
        items.append({
            "type": "url",
            "kind": "yt" if host in {"youtube.com", "youtu.be"} else "url",
            "label": line,
            "key": line.rstrip("/").lower(),
            "host": host,
            "ext_ok": True,
            "size_kb": 0,
        })
    return items


def analyse(items: list[dict]) -> list[str]:
    warnings: list[str] = []
    seen_keys: dict[str, int] = {}
    host_counts: dict[str, list[int]] = {}

    for i, it in enumerate(items, 1):
        if it["key"] in seen_keys and it["key"] != "unreadable":
            warnings.append(f"#{i:02d} {it['label']!r} duplicates #{seen_keys[it['key']]:02d}")
        else:
            seen_keys[it["key"]] = i

        if not it["ext_ok"]:
            warnings.append(f"#{i:02d} {it['label']!r} — NotebookLM won't accept this file type")

        host = it.get("host")
        if host:
            host_counts.setdefault(host, []).append(i)
            if host in LOW_VALUE_HOSTS:
                warnings.append(f"#{i:02d} {host} — usually a weak *primary* source; prefer the thing it's writing about")

    for host, idxs in host_counts.items():
        if len(idxs) >= 3:
            warnings.append(f"{host} appears {len(idxs)}× (#{', #'.join(f'{i:02d}' for i in idxs)}) — likely near-duplicates, keep the best")

    if len(items) > FREE_TIER_CAP:
        warnings.append(f"{len(items)} sources exceeds the free-tier cap of {FREE_TIER_CAP} — prune before uploading")
    return warnings


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", type=Path, help="folder of files to upload")
    ap.add_argument("--urls", type=Path, help="text file, one URL per line")
    ap.add_argument("--check", action="store_true", help="print only the warnings")
    a = ap.parse_args()
    if not a.dir and not a.urls:
        ap.error("give --dir and/or --urls")

    items: list[dict] = []
    if a.dir:
        if not a.dir.is_dir():
            sys.exit(f"not a directory: {a.dir}")
        items += scan_dir(a.dir)
    if a.urls:
        if not a.urls.is_file():
            sys.exit(f"not a file: {a.urls}")
        items += scan_urls(a.urls)

    warnings = analyse(items)

    if not a.check:
        print(f"\nNOTEBOOKLM SOURCE MANIFEST  —  {len(items)} sources")
        print("-" * 60)
        warn_idx = {int(w[1:3]) for w in warnings if w[:1] == "#"}
        for i, it in enumerate(items, 1):
            flag = "  <-- see warnings" if i in warn_idx else ""
            extra = f"  ({it['host']})" if it.get("host") else ""
            print(f" {i:02d}  [{it['kind']:<4}]  {it['label']}{extra}{flag}")
        n_file = sum(1 for it in items if it["type"] == "file")
        n_url = len(items) - n_file
        print("-" * 60)
        print(f"Sources: {n_file} files, {n_url} urls   ·   free-tier cap: {FREE_TIER_CAP}")

    if warnings:
        print(f"\n{'WARNINGS' if a.check else ''}  {len(warnings)} issue(s) — review before uploading:")
        for w in warnings:
            print(f"  ! {w}")
    else:
        print("\nNo issues — clean set.")

    _demo_ok()


def _demo_ok() -> None:
    """ponytail: self-check the dedupe + host-count logic (runs on every call, cheap)."""
    fake = [
        {"type": "url", "kind": "url", "label": "a", "key": "k1", "host": "nvidia.com", "ext_ok": True, "size_kb": 0},
        {"type": "url", "kind": "url", "label": "b", "key": "k1", "host": "nvidia.com", "ext_ok": True, "size_kb": 0},
        {"type": "url", "kind": "url", "label": "c", "key": "k3", "host": "nvidia.com", "ext_ok": True, "size_kb": 0},
        {"type": "file", "kind": "unsupported", "label": "x.key", "key": "k4", "ext_ok": False, "size_kb": 1},
    ]
    w = analyse(fake)
    assert any("duplicates #01" in x for x in w), w
    assert any("nvidia.com appears 3" in x for x in w), w
    assert any("won't accept" in x for x in w), w


if __name__ == "__main__":
    main()
