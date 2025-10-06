"""Configuration loading utilities for the contribution adder service."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Mapping

try:  # pragma: no cover - optional dependency handling
    from dotenv import load_dotenv
except ModuleNotFoundError:  # pragma: no cover - executed when extra is not installed
    load_dotenv = None  # type: ignore[assignment]

ENV_TARGET_REPO = "TARGET_REPO"
ENV_TOKEN = "CONTRIB_PAT"


@dataclass(slots=True)
class AppConfig:
    """Concrete settings required to run the contribution adder workflow."""

    target_repo: str
    token: str


def _load_dotenv_if_available(dotenv_path: str | os.PathLike[str] | None) -> None:
    """Load environment variables from a ``.env`` file when python-dotenv is installed."""

    if load_dotenv is None:
        return

    candidate = Path(dotenv_path) if dotenv_path is not None else Path.cwd() / ".env"
    if candidate.exists():
        load_dotenv(dotenv_path=str(candidate), override=False)


def load_config(
    env: Mapping[str, str] | None = None,
    *,
    dotenv_path: str | os.PathLike[str] | None = None,
) -> AppConfig:
    """Load configuration from environment variables and optional ``.env`` file.

    Parameters
    ----------
    env:
        Optional mapping used for environment lookups. When provided, ``os.environ``
        is not read, enabling deterministic tests.
    dotenv_path:
        Explicit path to a ``.env`` file. When omitted, the loader searches for a
        file named ``.env`` in the current working directory.

    Returns
    -------
    AppConfig
        A populated configuration object.

    Raises
    ------
    RuntimeError
        If any required variables are missing.
    """

    if env is None:
        _load_dotenv_if_available(dotenv_path)
        env_mapping: Mapping[str, str] = os.environ
    else:
        env_mapping = env

    target_repo = env_mapping.get(ENV_TARGET_REPO)
    token = env_mapping.get(ENV_TOKEN)

    missing = [name for name, value in ((ENV_TARGET_REPO, target_repo), (ENV_TOKEN, token)) if not value]
    if missing:
        missing_list = ", ".join(missing)
        raise RuntimeError(
            "Missing required environment variable(s): "
            f"{missing_list}. Ensure they are set or provided via a .env file."
        )

    return AppConfig(target_repo=target_repo or "", token=token or "")


__all__ = ["AppConfig", "ENV_TARGET_REPO", "ENV_TOKEN", "load_config"]
