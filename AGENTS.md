# Repository-wide Agent Instructions

## General Goals
- Produce robust, modular, and maintainable code.
- Favor clarity, type annotations, and docstrings for all public functions and classes.
- Ensure every Python module includes unit tests when feasible.
- Prefer standard library solutions before introducing third-party dependencies.
- Keep commits focused and well-documented.

## Code Style
- Follow PEP 8 and PEP 257 conventions.
- Use `logging` instead of `print` for runtime information.
- Handle errors explicitly; avoid broad `except Exception` clauses.
- Do not suppress linter warnings without justification.
- Keep functions small and purpose-driven; refactor when logic becomes complex.

## Testing
- All new functionality must be accompanied by `pytest`-based tests under the `tests/` directory.
- Mock external services (e.g., network, GitHub) in tests.
- Tests must be deterministic and not depend on real credentials or network access.
- Provide fixtures for shared setup when appropriate.

## Documentation
- Update relevant documentation (e.g., `README.md`, module docstrings) when behavior changes.
- Include comments explaining non-obvious logic.

## Tooling
- Prefer `pip`-based workflows unless a task explicitly calls for alternatives.
- Keep configuration files minimal and well-commented.

## Repository Structure
- Place application code under `src/contribution_adder/`.
- Place automation workflows under `.github/workflows/`.
- Ensure configuration files (e.g., `pyproject.toml`, `pytest.ini`) live at the repository root unless directed otherwise.

Follow these instructions for all files within this repository unless a nested `AGENTS.md` overrides them.
