"""Deliver the finished front page to the grader's output folder.

The picture itself was composed earlier and lives beside this script as
``entry.png``.  Nothing here draws, downloads, or invents anything: this
script simply hands the exact stored bytes to the harness, so every run
produces the identical file.  It reads one environment setting,
``MAKEFUN_OUTPUT_DIR``, and falls back to ``/output`` when the harness
does not set it.
"""

from __future__ import annotations

import hashlib
import os
import shutil
from pathlib import Path

PICTURE_NAME = "entry.png"
DEFAULT_TARGET_DIR = "/output"
COPY_CHUNK = 1024 * 1024


def picture_next_to_script() -> Path:
    """Where the stored picture lives: the folder holding this script."""
    return Path(__file__).resolve().parent / PICTURE_NAME


def target_folder() -> Path:
    """Where the harness wants the picture, from the environment or default."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_TARGET_DIR
    return Path(chosen)


def move_bytes(source: Path, destination: Path) -> int:
    """Stream ``source`` into ``destination`` untouched; return byte count."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    with source.open("rb") as incoming, destination.open("wb") as outgoing:
        shutil.copyfileobj(incoming, outgoing, length=COPY_CHUNK)
    return destination.stat().st_size


def fingerprint(path: Path) -> str:
    """SHA-256 hex digest of the file at ``path``, read in chunks."""
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for piece in iter(lambda: handle.read(COPY_CHUNK), b""):
            hasher.update(piece)
    return hasher.hexdigest()


def run() -> None:
    """Copy the picture into place and print where it landed and its hash.

    The copy is a plain byte stream: no decoding, no re-encoding, so the
    output is byte-identical to the stored picture on every run.
    """
    source = picture_next_to_script()
    if not source.is_file():
        raise SystemExit(f"missing picture next to script: {source}")
    destination = target_folder() / PICTURE_NAME
    size = move_bytes(source, destination)
    print(f"wrote {destination} ({size} bytes, sha256={fingerprint(destination)})")


if __name__ == "__main__":
    run()
