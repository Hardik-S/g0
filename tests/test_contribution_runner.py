"""Tests for the :mod:`contribution_adder.contribution_runner` module."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

import pytest
from git import GitCommandError, Repo
from git.remote import Remote

from contribution_adder.config import AppConfig
from contribution_adder.contribution_runner import ContributionRunner, RunnerDependencies


def _config_loader_factory(target_repo: str, token: str) -> Callable[[], AppConfig]:
    def _loader() -> AppConfig:
        return AppConfig(target_repo=target_repo, token=token)

    return _loader


def test_runner_creates_expected_commits(tmp_path: Path) -> None:
    remote_path = tmp_path / "remote.git"
    Repo.init(remote_path, bare=True)

    worktree = tmp_path / "worktree"
    dependencies = RunnerDependencies(
        config_loader=_config_loader_factory("example/repo", "token"),
        prime_picker=lambda seed: (2, 3),
        prime_summer=lambda pair: sum(pair),
        sleep=lambda seconds: None,
    )

    runner = ContributionRunner(
        worktree_dir=worktree,
        remote_override=str(remote_path),
        random_seed=42,
        dependencies=dependencies,
    )

    runner.run()

    log_path = worktree / "contribution-log.txt"
    lines = [line for line in log_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(lines) == 5

    remote_repo = Repo(remote_path)
    commit_count = int(remote_repo.git.rev_list("--count", "refs/heads/main"))
    assert commit_count == 5


def test_runner_retries_push(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    remote_path = tmp_path / "remote.git"
    Repo.init(remote_path, bare=True)
    worktree = tmp_path / "worktree"

    dependencies = RunnerDependencies(
        config_loader=_config_loader_factory("example/repo", "token"),
        prime_picker=lambda seed: (2, 3),
        prime_summer=lambda pair: 1,
        sleep=lambda seconds: None,
    )

    runner = ContributionRunner(
        worktree_dir=worktree,
        remote_override=str(remote_path),
        dependencies=dependencies,
        max_push_attempts=3,
    )

    attempts = {"count": 0}

    def fake_push(self: Remote, *args, **kwargs):
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise GitCommandError("push", 1, stderr="simulated failure")
        return []

    monkeypatch.setattr(Remote, "push", fake_push)

    runner.run()

    assert attempts["count"] == 3
