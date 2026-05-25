#!/usr/bin/env python3
"""
md_math_flavor.py

Convert Markdown display formulas between:

1. Generic Markdown / MathJax style:

   $$
   E = mc^2
   $$

2. GitHub-flavored Markdown math-fence style:

   ```math
   E = mc^2
   ```

Inline formulas such as `$x + y$` are intentionally left unchanged because
GitHub and most MathJax-based renderers support the same inline syntax.

The converter is conservative:
- it does not rewrite formulas inside ordinary code fences;
- it converts only standalone display math blocks or one-line display math;
- it preserves indentation around display math blocks, which is useful inside
  nested lists.

Usage examples:

    python md_math_flavor.py article.md --to github -o article.github.md
    python md_math_flavor.py article.github.md --to generic -o article.md
    python md_math_flavor.py article.md --to github --in-place
    python md_math_flavor.py article.md --to generic --check
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path


FENCE_RE = re.compile(r"^(?P<indent>[ \t]*)(?P<fence>`{3,}|~{3,})(?P<info>[^\n\r]*)$")
GENERIC_MATH_DELIM_RE = re.compile(r"^(?P<indent>[ \t]*)\$\$\s*$")
GENERIC_ONE_LINE_RE = re.compile(r"^(?P<indent>[ \t]*)\$\$(?P<body>.+?)\$\$\s*$")


def _split_keepends(text: str) -> list[str]:
    """Split while keeping line endings and preserving an empty file."""
    return text.splitlines(keepends=True)


def _line_ending(line: str) -> str:
    if line.endswith("\r\n"):
        return "\r\n"
    if line.endswith("\n"):
        return "\n"
    return ""


def _without_line_ending(line: str) -> str:
    if line.endswith("\r\n"):
        return line[:-2]
    if line.endswith("\n"):
        return line[:-1]
    return line


def _is_fence_close(line: str, fence_marker: str) -> bool:
    """
    Return True if `line` closes the currently open fenced block.

    Markdown permits closing fences with at least as many backticks/tildes as
    the opening fence and only whitespace after the fence.
    """
    stripped = _without_line_ending(line).lstrip(" \t")
    char = fence_marker[0]
    if not stripped.startswith(char * len(fence_marker)):
        return False
    rest = stripped[len(fence_marker):]
    return set(rest) <= {" ", "\t"}


def _fence_info_is_math(info: str) -> bool:
    """
    Detect GitHub math fences.

    Accepts:
      ```math
      ``` math
      ```math something

    The usual and recommended form is exactly ```math.
    """
    return info.strip().split(maxsplit=1)[0].lower() == "math" if info.strip() else False


def convert_generic_to_github(text: str) -> str:
    """
    Convert generic display math blocks delimited by $$ into GitHub math fences.

    Non-math code fences are copied unchanged. Existing GitHub math fences are
    also copied unchanged.
    """
    lines = _split_keepends(text)
    out: list[str] = []

    in_code_fence = False
    code_fence_marker = ""

    in_math_block = False
    math_indent = ""

    for line in lines:
        newline = _line_ending(line)
        raw = _without_line_ending(line)

        if in_math_block:
            if GENERIC_MATH_DELIM_RE.match(raw):
                out.append(f"{math_indent}```{newline}")
                in_math_block = False
            else:
                out.append(line)
            continue

        if in_code_fence:
            out.append(line)
            if _is_fence_close(line, code_fence_marker):
                in_code_fence = False
                code_fence_marker = ""
            continue

        fence_match = FENCE_RE.match(raw)
        if fence_match:
            # Preserve all existing fenced blocks, including existing ```math blocks.
            out.append(line)
            in_code_fence = True
            code_fence_marker = fence_match.group("fence")
            continue

        one_line = GENERIC_ONE_LINE_RE.match(raw)
        if one_line:
            indent = one_line.group("indent")
            body = one_line.group("body").strip()
            out.append(f"{indent}```math{newline or '\n'}")
            out.append(f"{indent}{body}{newline or '\n'}")
            out.append(f"{indent}```{newline}")
            continue

        delim = GENERIC_MATH_DELIM_RE.match(raw)
        if delim:
            math_indent = delim.group("indent")
            out.append(f"{math_indent}```math{newline or '\n'}")
            in_math_block = True
            continue

        out.append(line)

    # If the source has an unterminated $$ block, preserve the already emitted
    # opening fence and leave content as-is. This makes the problem visible in
    # the output rather than silently dropping anything.
    return "".join(out)


def convert_github_to_generic(text: str) -> str:
    """
    Convert GitHub ```math fenced blocks into generic $$ display math blocks.

    Non-math code fences are copied unchanged.
    """
    lines = _split_keepends(text)
    out: list[str] = []

    in_code_fence = False
    code_fence_marker = ""

    in_math_fence = False
    math_fence_marker = ""
    math_indent = ""

    for line in lines:
        newline = _line_ending(line)
        raw = _without_line_ending(line)

        if in_math_fence:
            if _is_fence_close(line, math_fence_marker):
                out.append(f"{math_indent}$${newline}")
                in_math_fence = False
                math_fence_marker = ""
                math_indent = ""
            else:
                out.append(line)
            continue

        if in_code_fence:
            out.append(line)
            if _is_fence_close(line, code_fence_marker):
                in_code_fence = False
                code_fence_marker = ""
            continue

        fence_match = FENCE_RE.match(raw)
        if fence_match:
            fence = fence_match.group("fence")
            info = fence_match.group("info")
            if fence.startswith("`") and _fence_info_is_math(info):
                math_indent = fence_match.group("indent")
                math_fence_marker = fence
                out.append(f"{math_indent}$${newline or '\n'}")
                in_math_fence = True
            else:
                out.append(line)
                in_code_fence = True
                code_fence_marker = fence
            continue

        out.append(line)

    # If the source has an unterminated ```math block, preserve the already
    # emitted opening $$ and copied body. The malformed input remains visible.
    return "".join(out)


def convert_text(text: str, target: str) -> str:
    if target == "github":
        return convert_generic_to_github(text)
    if target == "generic":
        return convert_github_to_generic(text)
    raise ValueError(f"Unsupported target: {target}")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert Markdown display math between GitHub ```math fences and generic $$ blocks."
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Input Markdown file.",
    )
    parser.add_argument(
        "--to",
        choices=("github", "generic"),
        required=True,
        help="Target Markdown formula flavor.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output Markdown file. Required unless --in-place or --check is used.",
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Rewrite the input file in place.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Do not write files. Exit 0 if no changes are needed, 1 otherwise. Prints a unified diff.",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="File encoding. Default: utf-8.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)

    if args.in_place and args.output:
        print("error: use either --in-place or --output, not both", file=sys.stderr)
        return 2

    if not args.in_place and not args.output and not args.check:
        print("error: --output is required unless --in-place or --check is used", file=sys.stderr)
        return 2

    source_path: Path = args.input
    if not source_path.exists():
        print(f"error: input file does not exist: {source_path}", file=sys.stderr)
        return 2

    original = source_path.read_text(encoding=args.encoding)
    converted = convert_text(original, args.to)

    if args.check:
        if original == converted:
            return 0

        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            converted.splitlines(keepends=True),
            fromfile=str(source_path),
            tofile=f"{source_path} ({args.to})",
        )
        sys.stdout.writelines(diff)
        return 1

    output_path = source_path if args.in_place else args.output
    assert output_path is not None
    output_path.write_text(converted, encoding=args.encoding)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
