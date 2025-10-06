"""Top-level package for the contribution adder project."""

from importlib import metadata

__all__ = ["__version__"]


def _get_version() -> str:
    """Return the installed package version or a default placeholder."""
    try:
        return metadata.version("contribution-adder")
    except metadata.PackageNotFoundError:  # pragma: no cover - fallback for editable installs
        return "0.0.0"


__version__ = _get_version()
