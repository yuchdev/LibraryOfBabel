"""Tests for vocabulary downloader (no real network requests)."""

from __future__ import annotations

import io
import urllib.error
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from babel.vocabulary.downloader import download_file


def _make_response(body: bytes, content_length: int | None = None) -> MagicMock:
    """Create a mock HTTP response object."""
    response = MagicMock()
    stream = io.BytesIO(body)
    response.read.side_effect = stream.read
    headers = MagicMock()
    headers.get.return_value = str(content_length) if content_length is not None else None
    response.headers = headers
    response.__enter__ = lambda s: s
    response.__exit__ = MagicMock(return_value=False)
    return response


@patch("urllib.request.urlopen")
def test_download_writes_file(mock_urlopen: MagicMock, tmp_path: Path) -> None:
    content = b"hello\nworld\n"
    mock_urlopen.return_value = _make_response(content, len(content))

    dest = tmp_path / "words.txt"
    result = download_file("https://example.com/words.txt", dest, show_progress=False)

    assert result == dest
    assert dest.exists()
    assert dest.read_bytes() == content


@patch("urllib.request.urlopen")
def test_download_creates_parent_dirs(mock_urlopen: MagicMock, tmp_path: Path) -> None:
    content = b"data"
    mock_urlopen.return_value = _make_response(content)

    dest = tmp_path / "nested" / "deep" / "file.txt"
    download_file("https://example.com/file.txt", dest, show_progress=False)

    assert dest.exists()


@patch("urllib.request.urlopen")
def test_download_empty_response_raises(mock_urlopen: MagicMock, tmp_path: Path) -> None:
    mock_urlopen.return_value = _make_response(b"")

    dest = tmp_path / "empty.txt"
    with pytest.raises(RuntimeError, match="empty"):
        download_file("https://example.com/empty.txt", dest, show_progress=False)


@patch("urllib.request.urlopen")
def test_download_cleans_up_tmp_on_network_error(
    mock_urlopen: MagicMock, tmp_path: Path
) -> None:
    mock_urlopen.side_effect = urllib.error.URLError("connection refused")

    dest = tmp_path / "words.txt"
    tmp = dest.with_suffix(".txt.tmp")

    with pytest.raises(RuntimeError, match="Download failed"):
        download_file("https://example.com/words.txt", dest, show_progress=False)

    assert not tmp.exists()
    assert not dest.exists()


@patch("urllib.request.urlopen")
def test_download_atomic_write_no_partial_file_on_empty(
    mock_urlopen: MagicMock, tmp_path: Path
) -> None:
    """An empty download must not leave any file behind."""
    mock_urlopen.return_value = _make_response(b"")

    dest = tmp_path / "words.txt"
    with pytest.raises(RuntimeError):
        download_file("https://example.com/words.txt", dest, show_progress=False)

    assert not dest.exists()


@patch("urllib.request.urlopen")
def test_download_with_progress_mode(mock_urlopen: MagicMock, tmp_path: Path) -> None:
    """show_progress=True must not raise in test environment."""
    content = b"word1\nword2\n"
    mock_urlopen.return_value = _make_response(content, len(content))

    dest = tmp_path / "words.txt"
    # Progress bar writes to a terminal; it should not crash in tests.
    download_file("https://example.com/words.txt", dest, show_progress=True)
    assert dest.read_bytes() == content
