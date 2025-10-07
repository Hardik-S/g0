"""Command line interface for the contribution adder package."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Sequence

from .contribution_runner import ContributionRunner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the contribution adder workflow.")
    parser.add_argument("--seed", type=int, default=None, help="Optional RNG seed for deterministic commit counts.")
    parser.add_argument(
        "--worktree",
        type=Path,
        default=None,
        help="Directory used for the cached repository clone (defaults to .cache/contribution_repo).",
    )
    parser.add_argument(
        "--branch",
        default="main",
        help="Branch name the runner should operate on (defaults to main).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = build_parser()
    args = parser.parse_args(argv)

    runner = ContributionRunner(worktree_dir=args.worktree, random_seed=args.seed, default_branch=args.branch)
    runner.run()


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
