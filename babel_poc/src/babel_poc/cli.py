from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from babel_poc.constants import (
    BORGES_ALPHABET_SIZE,
    BORGES_CHAR_SLOTS,
    BORGES_LOG10_SIZE,
    BORGES_PAGES,
    DEFAULT_PUNCTUATION,
    OBSERVABLE_UNIVERSE_PLANCK_VOLUMES_LOG10,
    UNIVERSE_ATOMS_LOG10,
)
from babel_poc.generators.base import BookConfig, LibraryGenerator
from babel_poc.generators.fixed_sentence import FixedSentenceGenerator
from babel_poc.generators.no_adjacent_punctuation import NoAdjacentPunctuationGenerator
from babel_poc.generators.pos_template import POSTemplateGenerator
from babel_poc.generators.unrestricted_words import UnrestrictedWordsGenerator
from babel_poc.mathlib.logmath import scientific_from_log10
from babel_poc.mathlib.metrics import calculate_metrics
from babel_poc.rendering.page_renderer import wrap_text
from babel_poc.vocabulary.loader import load_words
from babel_poc.vocabulary.models import VocabularyInfo
from babel_poc.vocabulary.normalizer import normalize_words

app = typer.Typer(
    name="babel-poc",
    help="Local Python PoC for Progressive Library of Babel Reduction.",
    add_completion=False,
)
console = Console()


def _load_vocab(vocab_path: Path) -> tuple[list[str], list[str]]:
    """Load and normalize vocabulary, return (words, punctuation)."""
    raw = load_words(vocab_path)
    words = normalize_words(raw, lowercase=True, reject_spaces=True)
    return words, DEFAULT_PUNCTUATION


def _make_generators(words: list[str], punctuation: list[str]) -> list[LibraryGenerator]:
    return [
        UnrestrictedWordsGenerator(words, punctuation),
        NoAdjacentPunctuationGenerator(words, punctuation),
        FixedSentenceGenerator(words, punctuation),
        POSTemplateGenerator(words, punctuation),
    ]


@app.command("info")
def cmd_info() -> None:
    """Print Borges base size, universe constants, and available modes."""
    console.rule("[bold]Library of Babel — PoC Info[/bold]")
    m, e = scientific_from_log10(BORGES_LOG10_SIZE)
    console.print("\n[bold]Borges Original Library[/bold]")
    console.print(f"  Pages per book    : {BORGES_PAGES}")
    console.print(f"  Alphabet size     : {BORGES_ALPHABET_SIZE}")
    console.print(f"  Character slots   : {BORGES_CHAR_SLOTS:,}")
    console.print(f"  log10(size)       : {BORGES_LOG10_SIZE:,.5f}")
    console.print(f"  Size              : ~{m:.3f} × 10^{e:,}")

    console.print("\n[bold]Universe Constants[/bold]")
    console.print(f"  Atoms in obs. universe  : ~10^{UNIVERSE_ATOMS_LOG10:.0f}")
    console.print(
        "  Planck volumes          : "
        f"~10^{OBSERVABLE_UNIVERSE_PLANCK_VOLUMES_LOG10:.0f}"
    )

    console.print("\n[bold]Available Modes[/bold]")
    modes = [
        (
            "unrestricted-words",
            "Each token can be any word or punctuation independently.",
        ),
        (
            "no-adjacent-punctuation",
            "No two punctuation tokens appear consecutively.",
        ),
        (
            "fixed-sentence",
            "Every sentence has exactly 15 words + end punctuation.",
        ),
        ("pos-template", "Tokens follow a POS template (DET ADJ NOUN VERB ...)."),
    ]
    for mode_id, desc in modes:
        console.print(f"  [cyan]{mode_id}[/cyan]  — {desc}")


@app.command("vocab-info")
def cmd_vocab_info(
    vocab: Path = typer.Option(..., "--vocab", help="Path to vocabulary file"),
) -> None:
    """Print vocabulary statistics."""
    if not vocab.exists():
        console.print(f"[red]Vocabulary file not found: {vocab}[/red]")
        raise typer.Exit(1)
    words, punctuation = _load_vocab(vocab)
    info = VocabularyInfo(
        vocabulary_id=vocab.stem,
        path=vocab,
        word_count=len(words),
        punctuation_count=len(punctuation),
        normalized=True,
        lowercase=True,
    )
    console.rule(f"[bold]Vocabulary: {vocab}[/bold]")
    console.print(f"  Words loaded      : {info.word_count:,}")
    console.print(f"  Punctuation marks : {info.punctuation_count}")
    console.print(f"  Normalized        : {info.normalized}")
    console.print(f"  Lowercase         : {info.lowercase}")
    console.print(f"  Punctuation       : {DEFAULT_PUNCTUATION}")


@app.command("metrics")
def cmd_metrics(
    mode: str = typer.Option("unrestricted-words", "--mode", help="Generation mode"),
    vocab: Path = typer.Option(..., "--vocab", help="Path to vocabulary file"),
    tokens_per_page: int = typer.Option(320, "--tokens-per-page"),
    pages: int = typer.Option(410, "--pages"),
) -> None:
    """Calculate and display Library size metrics."""
    if not vocab.exists():
        console.print(f"[red]Vocabulary file not found: {vocab}[/red]")
        raise typer.Exit(1)
    generators = _generators_by_id(*_load_vocab(vocab))
    if mode not in generators:
        console.print(f"[red]Unknown mode: {mode}. Choose from: {list(generators)}[/red]")
        raise typer.Exit(1)
    gen = generators[mode]
    log10_sz = gen.log10_size(pages=pages, tokens_per_page=tokens_per_page)
    metrics = calculate_metrics(mode, log10_sz)

    console.rule(f"[bold]Metrics — {gen.display_name}[/bold]")
    console.print(f"  Mode              : {metrics.mode_id}")
    console.print(f"  log10(size)       : {metrics.log10_size:,.5f}")
    console.print(f"  Size              : ~{metrics.mantissa:.3f} × 10^{metrics.exponent:,}")
    if metrics.log10_smaller_than_borges > 0:
        console.print(
            "  vs Borges         : "
            f"10^{metrics.log10_smaller_than_borges:,.0f} times [red]smaller[/red]"
        )
    else:
        console.print(
            "  vs Borges         : "
            f"10^{-metrics.log10_smaller_than_borges:,.0f} times [green]larger[/green]"
        )
    if metrics.log10_larger_than_universe_atoms > 0:
        console.print(
            "  vs universe atoms : "
            f"10^{metrics.log10_larger_than_universe_atoms:,.0f} times [green]larger[/green]"
        )
    else:
        console.print(
            "  vs universe atoms : "
            f"10^{-metrics.log10_larger_than_universe_atoms:,.0f} times [red]smaller[/red]"
        )


@app.command("page")
def cmd_page(
    mode: str = typer.Option("fixed-sentence", "--mode", help="Generation mode"),
    vocab: Path = typer.Option(..., "--vocab", help="Path to vocabulary file"),
    seed: str = typer.Option("demo-seed", "--seed", help="Book seed"),
    page: int = typer.Option(0, "--page", help="Page index (0-based)"),
    tokens_per_page: int = typer.Option(320, "--tokens-per-page"),
    pages: int = typer.Option(410, "--pages"),
) -> None:
    """Generate and display one page from a deterministic book."""
    if not vocab.exists():
        console.print(f"[red]Vocabulary file not found: {vocab}[/red]")
        raise typer.Exit(1)
    generators = _generators_by_id(*_load_vocab(vocab))
    if mode not in generators:
        console.print(f"[red]Unknown mode: {mode}[/red]")
        raise typer.Exit(1)
    gen = generators[mode]
    config = BookConfig(
        mode_id=mode,
        seed=seed,
        pages=pages,
        tokens_per_page=tokens_per_page,
        vocabulary_id=vocab.stem,
        punctuation=list(DEFAULT_PUNCTUATION),
    )
    log10_sz = gen.log10_size(pages=pages, tokens_per_page=tokens_per_page)
    metrics = calculate_metrics(mode, log10_sz)
    generated = gen.generate_page(config, page)

    console.rule(f"[bold]Library of Babel — Page {page}[/bold]")
    console.print(f"\n[bold]Mode:[/bold]  {gen.display_name}")
    console.print("\n[bold]Book:[/bold]")
    console.print(f"  seed           : {seed}")
    console.print(f"  page           : {page} / {pages}")
    console.print(f"  tokens per page: {tokens_per_page}")
    console.print("\n[bold]Metrics:[/bold]")
    console.print(f"  Library size   : ~{metrics.mantissa:.3f} × 10^{metrics.exponent:,}")
    if metrics.log10_smaller_than_borges > 0:
        console.print(
            "  Smaller than Borges : "
            f"10^{metrics.log10_smaller_than_borges:,.0f}"
        )
    console.print("\n[bold]Page:[/bold]")
    console.print(wrap_text(generated.text, width=80))


@app.command("compare")
def cmd_compare(
    vocab: Path = typer.Option(..., "--vocab", help="Path to vocabulary file"),
    _seed: str = typer.Option("demo-seed", "--seed"),
    _page: int = typer.Option(0, "--page"),
    tokens_per_page: int = typer.Option(320, "--tokens-per-page"),
    pages: int = typer.Option(410, "--pages"),
) -> None:
    """Compare all modes in a table."""
    if not vocab.exists():
        console.print(f"[red]Vocabulary file not found: {vocab}[/red]")
        raise typer.Exit(1)
    words, punctuation = _load_vocab(vocab)
    generators = _make_generators(words, punctuation)

    table = Table(title="Library of Babel — Mode Comparison", show_lines=True)
    table.add_column("Mode", style="cyan")
    table.add_column("log10(size)", justify="right")
    table.add_column("Size (scientific)", justify="right")
    table.add_column("vs Borges", justify="right")
    table.add_column("vs Universe atoms", justify="right")

    bm, be = scientific_from_log10(BORGES_LOG10_SIZE)
    table.add_row(
        "Original Borges",
        f"{BORGES_LOG10_SIZE:,.0f}",
        f"~{bm:.2f} × 10^{be:,}",
        "baseline",
        f"10^{BORGES_LOG10_SIZE - UNIVERSE_ATOMS_LOG10:,.0f} larger",
    )

    from babel_poc.progress.progress import progress_context

    with progress_context("Calculating metrics", len(generators)) as prog:
        for gen in generators:
            log10_sz = gen.log10_size(pages=pages, tokens_per_page=tokens_per_page)
            metrics = calculate_metrics(gen.mode_id, log10_sz)
            vs_borges = (
                f"10^{metrics.log10_smaller_than_borges:,.0f} smaller"
                if metrics.log10_smaller_than_borges > 0
                else f"10^{-metrics.log10_smaller_than_borges:,.0f} larger"
            )
            vs_atoms = (
                f"10^{metrics.log10_larger_than_universe_atoms:,.0f} larger"
                if metrics.log10_larger_than_universe_atoms > 0
                else f"10^{-metrics.log10_larger_than_universe_atoms:,.0f} smaller"
            )
            table.add_row(
                gen.display_name,
                f"{metrics.log10_size:,.0f}",
                f"~{metrics.mantissa:.2f} × 10^{metrics.exponent:,}",
                vs_borges,
                vs_atoms,
            )
            prog.advance(1)

    console.print(table)


def _generators_by_id(words: list[str], punctuation: list[str]) -> dict[str, LibraryGenerator]:
    return {generator.mode_id: generator for generator in _make_generators(words, punctuation)}


if __name__ == "__main__":
    app()
