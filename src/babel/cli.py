from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
import sys
from typer.main import get_command
from rich.console import Console
from rich.table import Table

from babel.constants import (
    BORGES_ALPHABET_SIZE,
    BORGES_CHAR_SLOTS,
    BORGES_LOG10_SIZE,
    BORGES_PAGES,
    DEFAULT_PUNCTUATION,
    OBSERVABLE_UNIVERSE_PLANCK_VOLUMES_LOG10,
    UNIVERSE_ATOMS_LOG10,
)
from babel.generators.base import BookConfig, LibraryGenerator
from babel.generators.borges_library import BorgesLibraryGenerator
from babel.generators.word_based import WordBasedGenerator
from babel.generators.punctuation_constrained import PunctuationConstrainedGenerator
from babel.generators.sentence_structured import SentenceStructuredGenerator
from babel.generators.grammar_constrained import GrammarConstrainedGenerator
from babel.generators.semantic_constrained import SemanticConstrainedGenerator
from babel.generators.topic_coherent import TopicCoherentGenerator
from babel.mathlib.logmath import scientific_from_log10
from babel.mathlib.metrics import calculate_metrics
from babel.rendering.page_renderer import wrap_text
from babel.vocabulary.discovery import VocabularyNotFoundError, resolve_vocabulary_path
from babel.vocabulary.installer import install_all_sources, install_source
from babel.vocabulary.loader import load_words
from babel.vocabulary.models import VocabularyInfo
from babel.vocabulary.normalizer import normalize_words

app = typer.Typer(
    name="library-of-babel",
    help="Local Python PoC for Progressive Library of Babel Reduction.",
    add_completion=False,
)
console = Console()


def _load_vocab(vocab_path: Path) -> tuple[list[str], list[str]]:
    """Load and normalize vocabulary, return (words, punctuation)."""
    raw = load_words(vocab_path)
    words = normalize_words(raw, lowercase=True, reject_spaces=True)
    return words, DEFAULT_PUNCTUATION


def _resolve_vocab(
    vocab: Optional[Path],
    vocab_source: Optional[str],
    auto_download: bool,
) -> Path:
    """Resolve vocabulary path; print actionable error and exit on failure."""
    try:
        return resolve_vocabulary_path(
            explicit_path=vocab,
            preferred_source=vocab_source,
            auto_download=auto_download,
        )
    except VocabularyNotFoundError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc


def _make_generators(words: list[str], punctuation: list[str]) -> list[LibraryGenerator]:
    return [
        BorgesLibraryGenerator(words, punctuation),
        WordBasedGenerator(words, punctuation),
        PunctuationConstrainedGenerator(words, punctuation),
        SentenceStructuredGenerator(words, punctuation),
        GrammarConstrainedGenerator(words, punctuation),
        SemanticConstrainedGenerator(words, punctuation),
        TopicCoherentGenerator(words, punctuation),
    ]


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
) -> None:
    """Main callback to handle custom help displaying all subcommand options."""
    if ctx.invoked_subcommand is None:
        # If the user didn't provide a subcommand, we show the full help by default.
        # But if they specifically asked for --help, Typer's default handler will
        # already have been triggered if we didn't disable it.
        # Since we want to display all sub-options for --help as well,
        # we can use a custom help formatter.
        pass

def _patch_typer_help() -> None:
    """Patch Typer to show all subcommand options in the main help message."""
    original_get_command = typer.main.get_command

    def patched_get_command(typer_app: typer.Typer) -> any:
        click_command = original_get_command(typer_app)
        original_format_help = click_command.format_help

        def patched_format_help(ctx: any, formatter: any) -> None:
            original_format_help(ctx, formatter)
            for name, command in click_command.commands.items():
                console.print(f"\n[bold]{'='*20} {name} {'='*20}[/bold]")
                with typer.Context(command, info_name=name, parent=ctx) as sub_ctx:
                    console.print(sub_ctx.get_help())

        click_command.format_help = patched_format_help
        return click_command

    typer.main.get_command = patched_get_command


_patch_typer_help()


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
        ("borges-library", "Character-based original model (English alphabet)."),
        ("word-based", "Each token can be any word or punctuation independently."),
        ("punctuation-constrained", "No two punctuation tokens appear consecutively."),
        ("sentence-structured", "Fixed-length sentences (15 words + end punct)."),
        ("grammar-constrained", "Tokens follow a POS template."),
        ("semantic-constrained", "Tokens are connected via semantic clusters."),
        ("topic-coherent", "Each book is restricted to a thematic manifold."),
    ]
    for mode_id, desc in modes:
        console.print(f"  [cyan]{mode_id}[/cyan]  — {desc}")


@app.command("vocab-info")
def cmd_vocab_info(
    vocab: Optional[Path] = typer.Option(None, "--vocab", help="Path to vocabulary file"),
    vocab_source: Optional[str] = typer.Option(
        None, "--vocab-source", help="Installed vocabulary source ID"
    ),
) -> None:
    """Print vocabulary statistics."""
    resolved = _resolve_vocab(vocab, vocab_source, auto_download=False)
    words, punctuation = _load_vocab(resolved)
    info = VocabularyInfo(
        vocabulary_id=resolved.stem,
        path=resolved,
        word_count=len(words),
        punctuation_count=len(punctuation),
        normalized=True,
        lowercase=True,
    )
    console.rule(f"[bold]Vocabulary: {resolved}[/bold]")
    console.print(f"  Words loaded      : {info.word_count:,}")
    console.print(f"  Punctuation marks : {info.punctuation_count}")
    console.print(f"  Normalized        : {info.normalized}")
    console.print(f"  Lowercase         : {info.lowercase}")
    console.print(f"  Punctuation       : {DEFAULT_PUNCTUATION}")


@app.command("metrics")
def cmd_metrics(
    mode: str = typer.Option("word-based", "--mode", help="Generation mode"),
    vocab: Optional[Path] = typer.Option(None, "--vocab", help="Path to vocabulary file"),
    vocab_source: Optional[str] = typer.Option(
        None, "--vocab-source", help="Installed vocabulary source ID"
    ),
    auto_download: bool = typer.Option(False, "--auto-download/--no-auto-download"),
    tokens_per_page: Optional[int] = typer.Option(None, "--tokens-per-page"),
    pages: int = typer.Option(410, "--pages"),
) -> None:
    """Calculate and display Library size metrics."""
    resolved = _resolve_vocab(vocab, vocab_source, auto_download)
    generators = _generators_by_id(*_load_vocab(resolved))
    if mode not in generators:
        console.print(f"[red]Unknown mode: {mode}. Choose from: {list(generators)}[/red]")
        raise typer.Exit(1)
    gen = generators[mode]

    # Default tokens_per_page: 3200 for Borges, 320 for others
    if tokens_per_page is None:
        tokens_per_page = 3200 if mode == "borges-library" else 320

    log10_sz = gen.log10_size(pages=pages, tokens_per_page=tokens_per_page)
    metrics = calculate_metrics(mode, log10_sz)

    console.rule(f"[bold]Metrics — {gen.display_name}[/bold]")
    console.print(f"  Mode              : {metrics.mode_id}")
    console.print(f"  log10(size)       : {metrics.log10_size:,.5f}")
    console.print(f"  Size              : ~{metrics.mantissa:.3f} × 10^{metrics.exponent:,}")
    if abs(metrics.log10_smaller_than_borges) < 0.1:
        console.print("  vs Borges         : [green]equal[/green]")
    elif metrics.log10_smaller_than_borges > 0:
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

    if metrics.log10_larger_than_planck_volumes > 0:
        console.print(
            "  vs universe Planck volumes: "
            f"10^{metrics.log10_larger_than_planck_volumes:,.0f} times [green]larger[/green]"
        )
    else:
        console.print(
            "  vs universe Planck volumes: "
            f"10^{-metrics.log10_larger_than_planck_volumes:,.0f} times [red]smaller[/red]"
        )


@app.command("page")
def cmd_page(
    mode: str = typer.Option("sentence-structured", "--mode", help="Generation mode"),
    vocab: Optional[Path] = typer.Option(None, "--vocab", help="Path to vocabulary file"),
    vocab_source: Optional[str] = typer.Option(
        None, "--vocab-source", help="Installed vocabulary source ID"
    ),
    auto_download: bool = typer.Option(False, "--auto-download/--no-auto-download"),
    seed: str = typer.Option("demo-seed", "--seed", help="Book seed"),
    page: int = typer.Option(0, "--page", help="Page index (0-based)"),
    tokens_per_page: Optional[int] = typer.Option(None, "--tokens-per-page"),
    pages: int = typer.Option(410, "--pages"),
) -> None:
    """Generate and display one page from a deterministic book."""
    resolved = _resolve_vocab(vocab, vocab_source, auto_download)
    generators = _generators_by_id(*_load_vocab(resolved))
    if mode not in generators:
        console.print(f"[red]Unknown mode: {mode}[/red]")
        raise typer.Exit(1)
    gen = generators[mode]

    # Default tokens_per_page: 3200 for Borges, 320 for others
    if tokens_per_page is None:
        tokens_per_page = 3200 if mode == "borges-library" else 320

    config = BookConfig(
        mode_id=mode,
        seed=seed,
        pages=pages,
        tokens_per_page=tokens_per_page,
        vocabulary_id=resolved.stem,
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
    if abs(metrics.log10_smaller_than_borges) < 0.1:
        console.print("  Size vs Borges : [green]equal[/green]")
    elif metrics.log10_smaller_than_borges > 0:
        console.print(
            "  Smaller than Borges : "
            f"10^{metrics.log10_smaller_than_borges:,.0f}"
        )
    console.print("\n[bold]Page:[/bold]")
    console.print(wrap_text(generated.text, width=80))


@app.command("compare")
def cmd_compare(
    vocab: Optional[Path] = typer.Option(None, "--vocab", help="Path to vocabulary file"),
    vocab_source: Optional[str] = typer.Option(
        None, "--vocab-source", help="Installed vocabulary source ID"
    ),
    auto_download: bool = typer.Option(False, "--auto-download/--no-auto-download"),
    _seed: str = typer.Option("demo-seed", "--seed"),
    _page: int = typer.Option(0, "--page"),
    tokens_per_page: int = typer.Option(320, "--tokens-per-page"),
    pages: int = typer.Option(410, "--pages"),
) -> None:
    """Compare all modes in a table."""
    resolved = _resolve_vocab(vocab, vocab_source, auto_download)
    words, punctuation = _load_vocab(resolved)
    generators = _make_generators(words, punctuation)

    table = Table(title="Library of Babel — Mode Comparison", show_lines=True)
    table.add_column("Mode", style="cyan")
    table.add_column("log10(size)", justify="right")
    table.add_column("Size (scientific)", justify="right")
    table.add_column("vs Borges", justify="right")
    table.add_column("vs Universe atoms", justify="right")
    table.add_column("vs Planck volumes", justify="right")

    bm, be = scientific_from_log10(BORGES_LOG10_SIZE)
    table.add_row(
        "Borges (1941 Edition)",
        f"{BORGES_LOG10_SIZE:,.0f}",
        f"~{bm:.2f} × 10^{be:,}",
        "baseline",
        f"10^{BORGES_LOG10_SIZE - UNIVERSE_ATOMS_LOG10:,.0f} larger",
        f"10^{BORGES_LOG10_SIZE - OBSERVABLE_UNIVERSE_PLANCK_VOLUMES_LOG10:,.0f} larger",
    )

    from babel.progress.progress import progress_context

    with progress_context("Calculating metrics", len(generators)) as prog:
        for gen in generators:
            # Default tokens_per_page: 3200 for Borges, 320 for others
            current_tpp = tokens_per_page
            if current_tpp == 320 and gen.mode_id == "borges-library":
                current_tpp = 3200

            log10_sz = gen.log10_size(pages=pages, tokens_per_page=current_tpp)
            metrics = calculate_metrics(gen.mode_id, log10_sz)
            
            if abs(metrics.log10_smaller_than_borges) < 0.1:
                vs_borges = "equal"
            else:
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
            vs_planck = (
                f"10^{metrics.log10_larger_than_planck_volumes:,.0f} larger"
                if metrics.log10_larger_than_planck_volumes > 0
                else f"10^{-metrics.log10_larger_than_planck_volumes:,.0f} smaller"
            )
            table.add_row(
                gen.display_name,
                f"{metrics.log10_size:,.0f}",
                f"~{metrics.mantissa:.2f} × 10^{metrics.exponent:,}",
                vs_borges,
                vs_atoms,
                vs_planck,
            )
            prog.advance(1)

    console.print(table)


@app.command("vocab-list-sources")
def cmd_vocab_list_sources() -> None:
    """List all known vocabulary sources and their installation status."""
    from babel.config import DEFAULT_VOCAB_DIR
    from babel.vocabulary.sources import KNOWN_VOCABULARY_SOURCES

    table = Table(title="Known Vocabulary Sources", show_lines=True)
    table.add_column("Source ID", style="cyan")
    table.add_column("Display Name")
    table.add_column("Status")
    table.add_column("Local Path")
    table.add_column("License")
    table.add_column("Homepage")

    for source_id, src in KNOWN_VOCABULARY_SOURCES.items():
        words_file = DEFAULT_VOCAB_DIR / src.local_subdir / "words.txt"
        if words_file.exists() and words_file.stat().st_size > 0:
            status = "[green]installed[/green]"
            local_path = str(words_file)
        else:
            status = "[yellow]missing[/yellow]"
            local_path = ""
        table.add_row(
            source_id,
            src.display_name,
            status,
            local_path,
            src.license_name or "—",
            src.homepage_url,
        )

    console.print(table)
    console.print(
        "\nTo install a source:  [cyan]library-of-babel setup-vocab --source SOURCE_ID[/cyan]"
    )
    console.print("To install all:       [cyan]library-of-babel setup-vocab --all[/cyan]")


@app.command("setup-vocab")
def cmd_setup_vocab(
    source: Optional[str] = typer.Option(None, "--source", help="Source ID to install"),
    all_sources: bool = typer.Option(False, "--all", help="Install all available sources"),
    force: bool = typer.Option(False, "--force", help="Re-download even if already installed"),
) -> None:
    """Download and install vocabulary sources."""
    from babel.vocabulary.sources import KNOWN_VOCABULARY_SOURCES

    if not source and not all_sources:
        console.print(
            "[red]Specify --source SOURCE_ID or --all.[/red]\n"
            "Available sources: " + ", ".join(KNOWN_VOCABULARY_SOURCES)
        )
        raise typer.Exit(1)

    if all_sources:
        console.print("[bold]Installing all available vocabulary sources…[/bold]")
        results = install_all_sources(force=force)
        for entry in results:
            console.print(
                f"  [green]✔[/green]  {entry.vocabulary_id}  "
                f"({entry.word_count:,} words)  →  {entry.path}"
            )
        if not results:
            console.print("[yellow]No sources with automatic download URLs found.[/yellow]")
    else:
        assert source is not None
        console.print(f"[bold]Installing vocabulary source: {source}[/bold]")
        try:
            entry = install_source(source, force=force)
        except (ValueError, NotImplementedError) as exc:
            console.print(f"[red]{exc}[/red]")
            raise typer.Exit(1) from exc
        console.print(
            f"  [green]✔[/green]  {entry.vocabulary_id}  "
            f"({entry.word_count:,} words)  →  {entry.path}"
        )


def _generators_by_id(words: list[str], punctuation: list[str]) -> dict[str, LibraryGenerator]:
    return {generator.mode_id: generator for generator in _make_generators(words, punctuation)}


if __name__ == "__main__":
    app()
