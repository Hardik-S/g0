"""High-level orchestration for generating automated contribution commits."""

from __future__ import annotations

from dataclasses import dataclass
import logging
from pathlib import Path
import time
from typing import Callable

from git import GitCommandError, Repo

from .config import AppConfig, load_config
from .primes import pick_two_primes, sum_primes

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class RunnerDependencies:
    """Convenience wrapper that groups injectable dependencies.

    Dependency injection keeps :class:`ContributionRunner` testable by allowing
    unit tests to replace components such as the configuration loader or prime
    utilities without resorting to monkeypatching global symbols.
    """

    config_loader: Callable[[], AppConfig] = load_config
    prime_picker: Callable[[int | None], tuple[int, int]] = pick_two_primes
    prime_summer: Callable[[tuple[int, int]], int] = sum_primes
    sleep: Callable[[float], None] = time.sleep


class ContributionRunner:
    """Coordinate cloning, committing, and pushing contributions to a repo."""

    def __init__(
        self,
        *,
        worktree_dir: str | Path | None = None,
        remote_override: str | None = None,
        default_branch: str = "main",
        random_seed: int | None = None,
        dependencies: RunnerDependencies | None = None,
        logger: logging.Logger | None = None,
        max_push_attempts: int = 3,
    ) -> None:
        self._worktree_dir = Path(worktree_dir) if worktree_dir else Path(".cache") / "contribution_repo"
        self._remote_override = remote_override
        self._default_branch = default_branch
        self._random_seed = random_seed
        self._deps = dependencies or RunnerDependencies()
        self._logger = logger or LOGGER
        self._max_push_attempts = max_push_attempts

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def run(self) -> None:
        """Execute the contribution workflow end-to-end."""

        config = self._deps.config_loader()
        repo = self._prepare_repository(config)
        self._ensure_user_config(repo)

        prime_pair = self._deps.prime_picker(self._random_seed)
        commit_count = self._deps.prime_summer(prime_pair)
        if commit_count <= 0:
            self._logger.info("Computed non-positive commit count; skipping run.")
            return

        self._logger.info("Generating %s commits based on prime pair %s.", commit_count, prime_pair)
        log_path = Path(repo.working_tree_dir or self._worktree_dir) / "contribution-log.txt"
        log_path.parent.mkdir(parents=True, exist_ok=True)

        for iteration in range(1, commit_count + 1):
            self._append_log_entry(log_path, iteration, commit_count)
            repo.index.add([str(log_path)])
            message = f"chore: automated contribution {iteration}/{commit_count}"
            repo.index.commit(message)
            self._logger.debug("Created commit %s/%s with message %s", iteration, commit_count, message)

        self._push_with_retries(repo)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _prepare_repository(self, config: AppConfig) -> Repo:
        """Clone the repository if needed and ensure the working tree is ready."""

        remote_url = self._build_remote_url(config)
        worktree = self._worktree_dir
        worktree.parent.mkdir(parents=True, exist_ok=True)

        if worktree.exists() and (worktree / ".git").exists():
            repo = Repo(worktree)
            self._logger.debug("Using existing repository at %s", worktree)
            origin = repo.remotes.origin
            origin.fetch()
        else:
            self._logger.info("Cloning repository %s into %s", config.target_repo, worktree)
            repo = Repo.clone_from(remote_url, worktree)
            origin = repo.remotes.origin

        self._checkout_branch(repo)
        self._pull_latest(origin)
        self._ensure_upstream(repo)
        return repo

    def _build_remote_url(self, config: AppConfig) -> str:
        if self._remote_override:
            return self._remote_override

        token = config.token
        sanitized_repo = config.target_repo
        if not sanitized_repo:
            raise RuntimeError("Target repository cannot be empty.")

        return f"https://{token}@github.com/{sanitized_repo}.git"

    def _checkout_branch(self, repo: Repo) -> None:
        branch = self._default_branch
        try:
            repo.git.checkout(branch)
        except GitCommandError:
            remote_branch = f"origin/{branch}"
            if remote_branch in {ref.name for ref in repo.refs}:
                repo.git.checkout("-B", branch, remote_branch)
            else:
                repo.git.checkout("-B", branch)

    def _pull_latest(self, origin) -> None:
        branch = self._default_branch
        remote_branch = f"origin/{branch}"
        try:
            remote_refs = {ref.name for ref in origin.refs}
            if remote_branch in remote_refs:
                origin.pull(branch)
        except GitCommandError as exc:
            self._logger.warning("Failed to pull latest changes: %s", exc)

    def _ensure_user_config(self, repo: Repo) -> None:
        config_writer = repo.config_writer()
        config_reader = repo.config_reader()
        try:
            config_reader.get_value("user", "name")
        except Exception:  # pragma: no cover - configparser edge cases
            config_writer.set_value("user", "name", "Contribution Adder Bot")
        try:
            config_reader.get_value("user", "email")
        except Exception:  # pragma: no cover - configparser edge cases
            config_writer.set_value("user", "email", "contribution-adder@example.com")

    def _append_log_entry(self, log_path: Path, iteration: int, total: int) -> None:
        from datetime import datetime, timezone

        timestamp = datetime.now(tz=timezone.utc).isoformat()
        entry = f"{timestamp} - automated contribution {iteration}/{total}"
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(entry + "\n")

    def _ensure_upstream(self, repo: Repo) -> None:
        branch = self._default_branch
        remote_branch = f"origin/{branch}"
        if remote_branch in {ref.name for ref in repo.refs}:
            try:
                repo.git.branch("--set-upstream-to", remote_branch, branch)
            except GitCommandError:
                self._logger.debug("Unable to set upstream for branch %s", branch)

    def _push_with_retries(self, repo: Repo) -> None:
        origin = repo.remotes.origin
        last_error: GitCommandError | None = None
        refspec = f"{self._default_branch}:{self._default_branch}"
        for attempt in range(1, self._max_push_attempts + 1):
            try:
                origin.push(refspec=refspec)
                self._logger.info("Pushed changes on attempt %s", attempt)
                return
            except GitCommandError as exc:
                last_error = exc
                self._logger.warning("Push attempt %s failed: %s", attempt, exc)
                if attempt < self._max_push_attempts:
                    delay = min(2 ** (attempt - 1), 30)
                    self._deps.sleep(delay)

        if last_error is not None:
            raise last_error


__all__ = ["ContributionRunner", "RunnerDependencies"]
