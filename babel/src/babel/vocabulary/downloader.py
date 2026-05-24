"""Vocabulary downloader — streaming download with progress bar."""

from __future__ import annotations

import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)


def download_file(
    url: str,
    destination: Path,
    *,
    show_progress: bool = True,
) -> Path:
    """
    Download *url* to *destination* with an optional progress bar.

    Uses an atomic write strategy: the file is first written to a ``.tmp``
    sibling and renamed on success.  The temporary file is removed if an
    error occurs.

    Returns the final *destination* path.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = destination.with_suffix(destination.suffix + ".tmp")

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "babel-poc/0.1 vocabulary-downloader"},
        )
        with urllib.request.urlopen(req, timeout=60) as response:  # noqa: S310
            total_bytes: Optional[int] = None
            content_length = response.headers.get("Content-Length")
            if content_length:
                try:
                    total_bytes = int(content_length)
                except ValueError:
                    pass

            if show_progress:
                _download_with_progress(response, tmp_path, total_bytes, url)
            else:
                _download_plain(response, tmp_path)

    except urllib.error.URLError as exc:
        _cleanup_tmp(tmp_path)
        raise RuntimeError(f"Download failed for {url!r}: {exc}") from exc
    except Exception:
        _cleanup_tmp(tmp_path)
        raise

    # Verify non-empty
    if tmp_path.stat().st_size == 0:
        _cleanup_tmp(tmp_path)
        raise RuntimeError(f"Downloaded file is empty: {url!r}")

    tmp_path.replace(destination)
    return destination


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_CHUNK = 65_536  # 64 KiB


def _download_with_progress(response: object, dest: Path, total: Optional[int], label: str) -> None:
    progress = Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        transient=True,
    )
    with progress:
        task = progress.add_task(f"Downloading {label}", total=total)
        with dest.open("wb") as fh:
            while True:
                chunk = response.read(_CHUNK)  # type: ignore[attr-defined]
                if not chunk:
                    break
                fh.write(chunk)
                progress.advance(task, len(chunk))


def _download_plain(response: object, dest: Path) -> None:
    with dest.open("wb") as fh:
        while True:
            chunk = response.read(_CHUNK)  # type: ignore[attr-defined]
            if not chunk:
                break
            fh.write(chunk)


def _cleanup_tmp(tmp_path: Path) -> None:
    try:
        if tmp_path.exists():
            tmp_path.unlink()
    except OSError:
        pass
