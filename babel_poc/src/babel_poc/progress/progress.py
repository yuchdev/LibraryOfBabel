from contextlib import contextmanager

from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn


@contextmanager
def progress_context(description: str, total: int):
    """Rich-based progress context manager."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        transient=True,
    ) as progress:
        task = progress.add_task(description, total=total)

        class _ProgressProxy:
            def advance(self, n: int = 1) -> None:
                progress.advance(task, n)

        yield _ProgressProxy()
